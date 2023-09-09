# Generated by Django 4.2.3 on 2023-09-09 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.transport', verbose_name='Транспорт'),
        ),
    ]
