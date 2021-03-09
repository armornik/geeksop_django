import os
# import json

from django.shortcuts import render

from mainapp.models import ProductCategory, Products

# Обращение к папке mainapp
dir_ = os.path.dirname(__file__)


# Create your views here.
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


def products(request, id=None):
    context = {
        'title': 'GeekShop - Каталог',
        'products': Products.objects.all(),
        'categories': ProductCategory.objects.all(),
    }

    # file_path = os.path.join(dir_, 'fixtures/data.json')
    # context = dict()
    # context.update(json.load(open(file_path, encoding='utf-8')))

    # with open('mainapp/fixtures/data.json', 'r') as f:
    #     context = json.load(f)

    return render(request, 'mainapp/products.html', context)
