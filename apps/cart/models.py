from django.db.models import Sum

from apps.users.models import User
from django.db import models
from apps.product.models import Product, Category


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)  # Замените на вашу модель товаров
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, verbose_name='cart')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    def total_amount(self):
        return self.items.aggregate(Sum('product__price'))['product__price__sum'] or 0

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f'{self.product.name}'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f'{self.product}'


class Banners(models.Model):
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now=True)
    link = models.CharField(default="http://127.0.0.1:8000/api/v1/categories/", max_length=100)
    category_id = models.CharField(f"{Category.pk}", max_length=700)

    def __str__(self):
        return f'{self.image}'

    class Meta:
        verbose_name = "Баннеры"
        verbose_name_plural = "Баннеры"
