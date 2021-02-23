from django.shortcuts import render
import json

# Create your views here.
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


def products(request):
    with open('mainapp/fixtures/data.json', 'r') as f:
        context = json.load(f)
    # context = {'title': 'GeekShop - Каталог',
    #            'products': [
    #                {'name': 'Худи черного цвета с монограммами adidas Originals', 'price': '6 090,00', 'card_text': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.', 'img_src': '/static/vendor/img/products/Adidas-hoodie.png'},
    #                {'name': 'Синяя куртка The North Face', 'price': '23 725,00', 'card_text': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.', 'img_src': '/static/vendor/img/products/Blue-jacket-The-North-Face.png'},
    #                {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN', 'price': '3 390,00', 'card_text': 'Материал с плюшевой текстурой. Удобный и мягкий.', 'img_src': '/static/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png'},
    #            ],
    #            'products_of_promotion': [
    #                {'name': 'Черный рюкзак Nike Heritage', 'price': '2 340,00', 'card_text': 'Плотная ткань. Легкий материал.', 'img_src': '/static/vendor/img/products/Black-Nike-Heritage-backpack.png'},
    #                {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex', 'price': '13 590,00', 'card_text': 'Гладкий кожаный верх. Натуральный материал.', 'img_src': '/static/vendor/img/products/Black-Dr-Martens-shoes.png'},
    #                {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN', 'price': '2 890,00', 'card_text': 'Легкая эластичная ткань сирсакер Фактурная ткань.', 'img_src': '/static/vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png'},
    #            ]
    #            }
    return render(request, 'mainapp/products.html', context)


def test_context(request):
    context = {
        'title': 'geekshop',
        'header': 'Добро пожаловать на сайт!',
        'username': 'Иван Иванов'
    }
    return render(request, 'mainapp/test-context.html', context)
