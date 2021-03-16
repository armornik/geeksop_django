import os
# import json

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mainapp.models import ProductCategory, Products

# Обращение к папке mainapp
# dir_ = os.path.dirname(__file__)


# Create your views here.
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page=1):
    # context = {
    #     'title': 'GeekShop - Каталог',
    #     'products': Products.objects.all()
    # }
    context = {
        'title': 'GeekShop - Каталог',
        'categories': ProductCategory.objects.all()
    }

    # Без пагинации (разбивки на страницы)
    # context.update({'products': Products.objects.filter(category_id=category_id)}) if category_id and category_id != 6
    # else context.update({'products': Products.objects.all()})

    # if category_id and category_id != 6:
    #     context.update({'products': Products.objects.filter(category_id=category_id)})
    # else:
    #     context.update({'products': Products.objects.all()})

    # С пагинацией (разбивкой на страницы, если много товаров)

    if category_id and category_id != 6:
        products = Products.objects.filter(category_id=category_id).order_by('price')
    else:
        products = Products.objects.all().order_by('price')

    # products - список, с которым работаем,
    # per_page - сколько объектов отображаем на странице
    paginator = Paginator(products, per_page=3)
    products_paginator = paginator.page(page)

    # try:
    #     # products - список, с которым работаем,
    #     # per_page - сколько объектов отображаем на странице
    #     paginator = Paginator(products, per_page=3)
    #     products_paginator = paginator.page(page)
    #
    # except PageNotAnInteger:
    #     products_paginator = paginator.page(1)
    # except EmptyPage:
    #     products_paginator = paginator.page(paginator.num_pages)

    context.update({'products': products_paginator})

    # file_path = os.path.join(dir_, 'fixtures/data.json')
    # context = dict()
    # context.update(json.load(open(file_path, encoding='utf-8')))

    # with open('mainapp/fixtures/data.json', 'r') as f:
    #     context = json.load(f)

    return render(request, 'mainapp/products.html', context)
