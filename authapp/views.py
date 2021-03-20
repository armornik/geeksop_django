from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
# from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
from authapp.models import User


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                # reverse - определяет путь к странице
                return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'authapp/login.html', context)


class RegisterCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_message = 'Вы успешно зарегистрировались'
    # reverse_lazy - для получения урла - для класса
    success_url = reverse_lazy('auth:login')


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


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class ProfileUpdateView(UpdateView):
    model = Basket
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('auth:profile')

    def get_context_data(self, **kwargs):
        # получаем контекст у родителя
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        # вносим необходимые изменения
        context['baskets'] = Basket.objects.filter(pk=self.kwargs.get('pk'))
        context['form'] = UserProfileForm(instance=self.kwargs.get('pk'))
        return context

    # def get_object(self):
    #     return get_object_or_404(User, pk=self.request.user.id)

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
