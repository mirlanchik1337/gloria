# Generated by Django 4.2.3 on 2023-09-03 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_cartitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='order',
            field=models.ForeignKey(blank=1, null=1, on_delete=django.db.models.deletion.CASCADE, to='cart.order'),
        ),
    ]
