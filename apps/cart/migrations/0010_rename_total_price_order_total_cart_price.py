# Generated by Django 4.2.3 on 2023-09-20 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_order_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_price',
            new_name='total_cart_price',
        ),
    ]