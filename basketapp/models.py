# Перед миграцией добавить basketapp in settings.py
# manage.py makemigrations
# manage.py migrate

from django.db import models

from mainapp.models import Products
from authapp.models import User


# Create your models here.
class Basket (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price
