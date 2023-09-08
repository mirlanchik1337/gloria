# Generated by Django 4.2.3 on 2023-09-08 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0022_remove_order_cart_items_cartitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type_of_order',
            field=models.CharField(choices=[('Доставка', 'Доставка'), ('Самовывоз', 'Самовывоз')], max_length=100, verbose_name='Тип заказа'),
        ),
        migrations.DeleteModel(
            name='TypeOfOrder',
        ),
    ]
