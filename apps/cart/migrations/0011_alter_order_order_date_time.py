# Generated by Django 4.2.3 on 2023-09-24 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_rename_total_price_order_total_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date_time',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Дата и время забора заказа'),
        ),
    ]