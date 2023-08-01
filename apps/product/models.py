from django.db import models
from apps.users.models import User
import pytils


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')
    image = models.ImageField(help_text="Загрузите картинку для категории",
                              blank=True, null=True)
    category_slug = models.SlugField(null=False, db_index=True, unique=True, verbose_name='URl', default='',
                                     help_text="Перед вводом названия категории очистите это поле")

    def save(self, *args, **kwargs):
        self.category_slug = pytils.translit.slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название подкатегории')
    image = models.ImageField(help_text="Загрузите картинку для категории",
                              blank=True, null=True)
    subcategory_slug = models.SlugField(null=False, db_index=True, unique=True, verbose_name='URl', default='',
                                        help_text="Перед вводом названия категории очистите это поле")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.subcategory_slug = pytils.translit.slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название товара', db_index=True)
    product_slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='URl', default='',
                                    help_text="Перед вводом названия продукта очистите это поле")
    image = models.ImageField(verbose_name='Картинка товара', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Введите цену")
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена со скидкой', null=False,
                                         blank=True, default=0)
    description = models.TextField(verbose_name='Описание товара', blank=True, null=True)
    is_hit = models.BooleanField(default=False, verbose_name='Хит товар')
    is_sale = models.BooleanField(default=False, verbose_name='Акционный товар')
    created = models.DateTimeField(auto_now_add=True , verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Кол-во товара')
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара')
    subcategories = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория товара',
                                      null=True, blank=True)

    class Meta:
        ordering = ('name', 'product_slug')
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        index_together = (('id', 'product_slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.product_slug = pytils.translit.slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.CharField(max_length=255, verbose_name="Комментарий")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'{self.product}_{self.user}_{self.text}'


class QuationsAnswers(models.Model):
    title = models.TextField(verbose_name="Вопрос", blank=True, null=True)
    description = models.TextField(verbose_name="Ответ", blank=True, null=True)

    class Meta:
        verbose_name = "Вопросы-Ответы"
        verbose_name_plural = "Вопросы-Ответы"

    def __str__(self):
        return self.title


class Stories(models.Model):
    image = models.ImageField(default='static/gloria.jpg')
    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"

    def __str__(self):
        return f'{self.created_at}'
