# Generated by Django 4.2.3 on 2023-08-09 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_second_subcategories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('id', 'name', 'product_slug'), 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
