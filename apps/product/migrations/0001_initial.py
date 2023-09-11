# Generated by Django 4.2.3 on 2023-09-10 08:52

import apps.product.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=100, null=True, verbose_name='Текст на шаре')),
                ('is_cart', models.BooleanField(default=False, verbose_name='Добавление надписи к шару')),
                ('price', models.IntegerField(default=0, verbose_name='price')),
            ],
            options={
                'verbose_name': 'Надпись на Шаре',
                'verbose_name_plural': 'Надпись на Шаре',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название категории')),
                ('image', models.ImageField(blank=True, help_text='Загрузите картинку для категории', null=True, upload_to=apps.product.utils.path_and_rename2)),
                ('category_slug', models.SlugField(default='', help_text='Перед вводом названия категории очистите это поле', unique=True, verbose_name='URl')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='FontSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(verbose_name='Размер шрифта')),
            ],
            options={
                'verbose_name': 'Размеры Надписи',
                'verbose_name_plural': 'Размеры Надписи',
            },
        ),
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.product.utils.path_and_rename)),
            ],
        ),
        migrations.CreateModel(
            name='PostCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=100, null=True, verbose_name='Текст на открытке для букетов')),
                ('is_cart', models.BooleanField(verbose_name='Добавление открытки к букету')),
            ],
            options={
                'verbose_name': 'Открытка',
                'verbose_name_plural': 'Открытка',
            },
        ),
        migrations.CreateModel(
            name='PostCardPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='Цена открытки')),
            ],
            options={
                'verbose_name': 'Цена открыток',
                'verbose_name_plural': 'Цена открыток',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Название товара')),
                ('product_slug', models.SlugField(default='', help_text='Перед вводом названия продукта очистите это поле', max_length=100, unique=True, verbose_name='URl')),
                ('price', models.DecimalField(decimal_places=2, help_text='Введите цену', max_digits=10, verbose_name='Цена')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание товара')),
                ('is_hit', models.BooleanField(default=False, verbose_name='Хит товар')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Кол-во товара')),
                ('volume', models.PositiveIntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ('id', 'name', 'product_slug'),
            },
        ),
        migrations.CreateModel(
            name='QuationsAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True, verbose_name='Вопрос')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Ответ')),
            ],
            options={
                'verbose_name': 'Вопросы-Ответы',
                'verbose_name_plural': 'Вопросы-Ответы',
            },
        ),
        migrations.CreateModel(
            name='Stories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='static/gloria.jpg', upload_to='')),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'Истории',
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('min_volume', models.PositiveIntegerField()),
                ('max_volume', models.PositiveIntegerField()),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name': 'Транспорт',
                'verbose_name_plural': 'Транспорты',
            },
        ),
        migrations.CreateModel(
            name='WhatsAppLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название подкатегории')),
                ('image', models.ImageField(blank=True, help_text='Загрузите картинку для подкатегории', null=True, upload_to=apps.product.utils.path_and_rename3)),
                ('subcategory_slug', models.SlugField(default='', help_text='Перед вводом названия подкатегории очистите это поле', unique=True, verbose_name='URl')),
                ('categories', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.CreateModel(
            name='SecondSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название второй подкатегории')),
                ('image', models.ImageField(blank=True, help_text='Загрузите картинку для подподкатегории', null=True, upload_to=apps.product.utils.path_and_rename4)),
                ('second_subcategory_slug', models.SlugField(default='', help_text='Перед вводом названия второй подкатегории очистите это поле', unique=True, verbose_name='URl')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Категория')),
                ('subcategories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.subcategory', verbose_name='Подкатегория')),
            ],
            options={
                'verbose_name': 'Вторая Подкатегория',
                'verbose_name_plural': 'Вторые Подкатегории',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Комментарий')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
