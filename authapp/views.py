from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket


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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            # messages.success - вывести сообщение в случае успешного создания пользователя
            messages.success(request, 'Вы успешно зарегистрировались')
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


# @login_required(login_url='/auth/login/') - если не использовать в settings LOGIN_URL
@login_required
def profile(request):
    if request.method == 'POST':
        # instance - с конкретным пользователем
        # files=request.FILES - работать с файлами
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    baskets = Basket.objects.filter(user=request.user)

    # variant_1
    # total_quantity = 0
    # total_sum = 0
    # for basket in baskets:
    #     total_quantity += basket.quantity
    #     total_sum += basket.sum()
    # context = {
    #     'form': form,
    #     'baskets': baskets,
    #     'total_quantity': total_quantity,
    #     'total_sum': total_sum
    # }

    # variant_2
    # total_quantity = sum(basket.quantity for basket in baskets)
    # total_sum = sum(basket.sum() for basket in baskets)
    # context = {
    #     'form': form,
    #     'baskets': baskets,
    #     'total_quantity': total_quantity,
    #     'total_sum': total_sum
    # }

    context = {
        'form': form,
        'baskets': baskets,
    }

    return render(request, 'authapp/profile.html', context)
