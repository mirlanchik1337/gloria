# Generated by Django 4.2.3 on 2023-07-31 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_category_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='added_text',
            field=models.BooleanField(default=False, verbose_name='Добавить текст да / нет'),
        ),
        migrations.AddField(
            model_name='product',
            name='text',
            field=models.TextField(default=0, max_length=150, verbose_name='текст для шаров'),
        ),
    ]
