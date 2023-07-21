from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название товара')
    price = models.IntegerField(verbose_name='Цена товара')
    discount_price = models.IntegerField(verbose_name='Цена со скидкой', blank=True, null=True)
    postcard = models.IntegerField(verbose_name='Открытка', default=25, blank=True, null=True)
    description = models.TextField(verbose_name='Описание товара', blank=True, null=True)
    is_hit = models.BooleanField(default=False, verbose_name='Хит товар')
    is_sale = models.BooleanField(default=False, verbose_name='Акционный товар')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Кол-во товара')
    categories = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория товара')
    subcategories = models.ForeignKey('Subcategory', on_delete=models.CASCADE, verbose_name='Подкатегория товара', null=True, blank=True)


    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')

    def __str__(self):
        return self.title

class Subcategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название подкатегории')

    def __str__(self):
        return self.title


