from apps.users.models import User
from django.db import models
from apps.product.models import Product, Category, Transport


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
    link = models.CharField(default="http://127.0.0.1:8000/api/v1/categories/", max_length=100)

    def __str__(self):
        return f'{self.image}'

    class Meta:
        verbose_name = "Баннеры"
        verbose_name_plural = "Баннеры"


class TypeOfOrder(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Тип заказа"
        verbose_name_plural = "Типы заказа"


class Filial(models.Model):
    name_address = models.CharField(max_length=150, verbose_name='Название филиала')

    def __str__(self):
        return f'{self.name_address}'

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=100, verbose_name='Имя заказчика')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    type_of_order = models.ForeignKey('TypeOfOrder', on_delete=models.CASCADE, verbose_name='Вид заказа')
    as_soon_as_possible = models.BooleanField(default=False, verbose_name='Как можно скорее')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания заказа')
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, verbose_name='Филиал')
    order_date_time = models.DateTimeField(verbose_name='Дата и время забора заказа', auto_created=True)
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=True, null=True)
    apartment = models.CharField(max_length=100, verbose_name='Дом/квартира', blank=True, null=True)
    floor_and_code = models.CharField(max_length=100, verbose_name='Этаж и код от домофона', blank=True, null=True)
    additional_to_order = models.CharField(max_length=200, verbose_name='Доп инфо к заказу', blank=True, null=True)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name='Транспорт')
    cart_items = models.ManyToManyField(CartItem)


    def __str__(self):
        return f'{self.person_name}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
