from django.db import models
# makemigrations - создать миграцию
# migrate - применить миграцию

# createsuperuser

# manage.py dumpdata mainapp.ProductCategory > categories.json - создать json  с данными
# manage.py dumpdata mainapp.Products > goods.json - создать json  с данными
# manage.py loaddata mainapp/fixtures/goods.json - восстановить данные

# manage.py shell - запустить консоль
# ProductCategory.objects.create(name='Новинки') - создать объект
# ProductCategory.objects.get(name='Новинки') - получить объект
# ProductCategory.objects.filter(id=3) - получить объект (не вызывает ошибки, если не существует)
# ProductCategory.objects.all() - получить все объекты


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    #  change name in table
    class Meta:
        verbose_name_plural = 'Product Categories'

    # Отоброжение имени класса
    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=64, blank=True)
    # decimal_places - сколько знаков после запятой
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    # upload_to - куда сохранить картинки (папка)
    image = models.ImageField(upload_to='products_images', blank=True)
    # CASCADE - при удалении категории, удалятся все продукты (PROTECT - если в категории есть продукты, то не удалится)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Products'

    # Отоброжение имени продукта
    def __str__(self):
        return f'{self.name} | {self.category.name}'
