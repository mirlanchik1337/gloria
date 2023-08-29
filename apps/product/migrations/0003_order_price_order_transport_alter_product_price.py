# Generated by Django 4.2.3 on 2023-08-27 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_filial_transport_typeoforder_product_volume_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Цена'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='transport',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.transport', verbose_name='Транспорт'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Введите цену', max_digits=10, verbose_name='Цена'),
        ),
    ]
