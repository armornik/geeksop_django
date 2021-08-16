# from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
# from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
from authapp.models import User


# Create your views here.
# login with CBV
class UserLoginView(LoginView):
    template_name = 'authapp/login.html'
    model = User
    form_class = UserLoginForm
    fields = ['username', 'password']


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 # reverse - определяет путь к странице
#                 return HttpResponseRedirect(reverse('index'))
#         else:
#             print(form.errors)
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'authapp/login.html', context)


class RegisterCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_message = 'Вы успешно зарегистрировались'
    # reverse_lazy - для получения урла - для класса
    success_url = reverse_lazy('auth:login')

    def get_context_data(self, **kwargs):
        context = super(RegisterCreateView, self).get_context_data()
        context['title'] = 'GeekShop - Регистрация'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            messages.success(self.request, 'Вы успешно зарегистрировались!')
            user = form.save()
            if send_verify_mail(user):
                print('success sending')
            else:
                print('sending failed')
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            messages.error(self.request, 'Такой пользователь или почта уже существуют!')
            return HttpResponseRedirect(reverse('authapp:register'))


# def verify(request, email, activation_key):
#     user = User.objects.filter(email=email).first()
#     if user:
#         if user.activation_key == activation_key and not user.is_activation_key_expired():
#             user.is_active = True
#             user.save()
#             auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             messages.success(request, "Учетная запись активирована")
#         return HttpResponseRedirect(reverse('authapp:verification'))
#     return HttpResponseRedirect(reverse('index'))
#
#
# def send_verify_mail(user):
#     subject = 'Verify your account'
#     verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
#     message = f'{settings.DOMAIN_NAME}{verify_link}'
#     return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username}, на сайте {settings.DOMAIN_NAME} ' \
              f'- пройдите по ссылке: ' \
              f'<a href="{settings.DOMAIN_NAME}{verify_link}"> Активировать </a>'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'activation key error in user: {user.username}')
            return render(request, 'authapp/verification.html')
    except Exception as err:
        print(f'Error activation user: {err.args}')
        return HttpResponseRedirect(reverse('index'))


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             # messages.success - вывести сообщение в случае успешного создания пользователя
#             messages.success(request, 'Вы успешно зарегистрировались')
#             return HttpResponseRedirect(reverse('auth:login'))
#         else:
#             print(form.errors)
#     else:
#         form = UserRegisterForm()
#     context = {'form': form}
#     return render(request, 'authapp/register.html', context)


class UserLogoutView(LogoutView):
    next_page = 'index'


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('auth:profile', kwargs={'pk': self.object.id})  # object because model = User

    def get_context_data(self, **kwargs):
        # получаем контекст у родителя
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        # вносим необходимые изменения
        context['baskets'] = Basket.objects.filter(user=self.object.id)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)


# # @login_required(login_url='/auth/login/') - если не использовать в settings LOGIN_URL
# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         # instance - с конкретным пользователем
#         # files=request.FILES - работать с файлами
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid:
#             form.save()
#             return HttpResponseRedirect(reverse('auth:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#     baskets = Basket.objects.filter(user=user)
#
#     # variant_1
#     # total_quantity = 0
#     # total_sum = 0
#     # for basket in baskets:
#     #     total_quantity += basket.quantity
#     #     total_sum += basket.sum()
#     # context = {
#     #     'form': form,
#     #     'baskets': baskets,
#     #     'total_quantity': total_quantity,
#     #     'total_sum': total_sum
#     # }
#
#     # variant_2
#     # total_quantity = sum(basket.quantity for basket in baskets)
#     # total_sum = sum(basket.sum() for basket in baskets)
#     # context = {
#     #     'form': form,
#     #     'baskets': baskets,
#     #     'total_quantity': total_quantity,
#     #     'total_sum': total_sum
#     # }
#
#     context = {
#         'form': form,
#         'baskets': baskets,
#     }
#
#     return render(request, 'authapp/profile.html', context)
