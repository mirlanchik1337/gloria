from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название подкатегории')

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название товара')
    image = models.ImageField(verbose_name='Картинка товара', null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена товара')
    discount_price = models.IntegerField(verbose_name='Цена со скидкой', blank=True, null=True)
    description = models.TextField(verbose_name='Описание товара', blank=True, null=True)
    is_hit = models.BooleanField(default=False, verbose_name='Хит товар')
    is_sale = models.BooleanField(default=False, verbose_name='Акционный товар')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Кол-во товара')
    categories = models.ForeignKey(Category, on_delete=models.CASCADE,  verbose_name='Категория товара', null=True, blank=True)
    subcategories = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория товара',
                                      null=True, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.CharField(max_length=255, verbose_name="Комментарий")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.product}_{self.user}_{self.text}'
