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
    image = models.ImageField(help_text="Загрузите картинку для подкатегории",
                              blank=True, null=True)
    subcategory_slug = models.SlugField(null=False, db_index=True, unique=True, verbose_name='URl', default='',
                                        help_text="Перед вводом названия подкатегории очистите это поле")
    categories = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория', default=1)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.subcategory_slug = pytils.translit.slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)


class SecondSubcategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название второй подкатегории')
    image = models.ImageField(help_text="Загрузите картинку для подподкатегории",
                              blank=True, null=True)
    second_subcategory_slug = models.SlugField(null=False, db_index=True, unique=True, verbose_name='URl', default='',
                                               help_text="Перед вводом названия второй подкатегории очистите это поле")
    categories = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    subcategories = models.ForeignKey('Subcategory', on_delete=models.CASCADE, verbose_name='Подкатегория')

    class Meta:
        verbose_name = "Вторая Подкатегория"
        verbose_name_plural = "Вторые Подкатегории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.second_subcategory_slug = pytils.translit.slugify(self.name)
        super(SecondSubcategory, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название товара', db_index=True)
    product_slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='URl', default='',
                                    help_text="Перед вводом названия продукта очистите это поле")
    image_1 = models.ImageField(verbose_name='Картинка товара', help_text='Картинка товара №1', null=True, blank=True)
    image_2 = models.ImageField(verbose_name='Картинка товара', help_text='Картинка товара №2', null=True, blank=True)
    image_3 = models.ImageField(verbose_name='Картинка товара', help_text='Картинка товара №3', null=True, blank=True)
    image_4 = models.ImageField(verbose_name='Картинка товара', help_text='Картинка товара №4', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Введите цену")
    description = models.TextField(verbose_name='Описание товара', blank=True, null=True)
    is_hit = models.BooleanField(default=False, verbose_name='Хит товар')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Кол-во товара', default=0)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара')
    subcategories = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория товара',
                                      null=True, blank=True)
    second_subcategories = models.ForeignKey(SecondSubcategory, on_delete=models.CASCADE,
                                             verbose_name='Вторая подкатегория товара', null=True, blank=True)

    class Meta:
        ordering = ('id', 'name', 'product_slug')
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


class WhatsAppLink(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class PostCardPrice(models.Model):
    price = models.IntegerField(verbose_name='Цена открытки')

    def __str__(self):
        return f'{self.price}'

    class Meta:
        verbose_name = "Цена открыток"
        verbose_name_plural = "Цена открыток"


class PostCard(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True, verbose_name='Текст на открытке для букетов')
    is_cart = models.BooleanField(default=False, verbose_name='Добавление открытки к букету')
    price = models.ForeignKey(PostCardPrice, on_delete=models.CASCADE, default=0, verbose_name='Цена открытки')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.user}_{self.product}_{self.text}'

    class Meta:
        verbose_name = "Открытка"
        verbose_name_plural = "Открытка"


class FontSize(models.Model):
    size = models.IntegerField(verbose_name='Размер шрифта')

    def __str__(self):
        return f'{self.size}'

    class Meta:
        verbose_name = "Размеры Надписи"
        verbose_name_plural = "Размеры Надписи"


class TitleOnBall(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True, verbose_name='Текст на шаре')
    is_cart = models.BooleanField(default=False, verbose_name='Добавление надписи к шару')
    size = models.ForeignKey(FontSize, on_delete=models.CASCADE, default=0, verbose_name='Размер шрифта')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.user}_{self.product}_{self.text}'

    class Meta:
        verbose_name = "Надпись на Шаре"
        verbose_name_plural = "Надпись на Шаре"
