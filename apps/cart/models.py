from apps.users.models import User
from django.db import models
from apps.product.models import Product


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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
    link = models.CharField(default="http://127.0.0.1:8000/api/v1/categories/", max_length=50)

    def __str__(self):
        return f'{self.image}'

    class Meta:
        verbose_name = "Баннеры"
        verbose_name_plural = "Баннеры"
