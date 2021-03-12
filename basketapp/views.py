from django.shortcuts import HttpResponseRedirect
# from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from basketapp.models import Basket
from mainapp.models import Products


# Create your views here.
@login_required
def basket_add(request, product_id=None):
    product = Products.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        basket = Basket(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
        # request.META.get('HTTP_REFERER') - страница на которой был выполнен запрос
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return HttpResponseRedirect(reverse('auth:profile'))
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# id - корзины (будет удаляться корзина вместе с продуктом)
def basket_delete(request, id=None):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        # получаем все объекты корзины с обновленными данными
        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        # render_to_string - в каком шаблоне (basketapp/basket.html) обновляем контекст
        result = render_to_string('basketapp/basket.html', context)
        return JsonResponse({'result': result})
