from django.db import models
from main.models import Category

class Balloon(models.Model):
    image_balloon = models.ImageField()
    title_balloon = models.CharField(max_length=130)
    description_balloon = models.TextField(max_length=300)
    price_balloon = models.IntegerField()
    is_hit = models.BooleanField()
    category = models.ManyToManyField(Category, verbose_name='category_product')



class SweetGift(models.Model):
    image_sweet = models.ImageField()
    name_sweet = models.CharField(max_length=60)
    description = models.TextField(max_length=255, default=None)
    price_sweet = models.IntegerField()
    is_hit = models.BooleanField()
    category = models.ManyToManyField(Category, verbose_name='category_product')
    def __str__(self):
        return self.name_sweet



class Postcard(models.Model):
    photo_postcard = models.ImageField()
    for_name = models.CharField(max_length=40)
    text = models.TextField(max_length=300)
    is_hit = models.BooleanField()
    category = models.ManyToManyField(Category, verbose_name='category_product')
    def __str__(self):
        return self.for_name


class Flowers(models.Model):
    image_flower = models.ImageField()
    name_product = models.CharField(max_length=60)
    description = models.TextField(max_length=300, null=True, blank=True)
    structure = models.CharField(max_length=120)
    price = models.IntegerField(unique=True)
    is_hit = models.BooleanField()
    category = models.ManyToManyField(Category, verbose_name='category_product')
    def __str__(self):
        return self.name_product


class Review(models.Model):
    text = models.CharField(max_length=255, verbose_name='Комментарий к продукту')
    product = models.ForeignKey('Flowers', on_delete=models.CASCADE)