# Generated by Django 4.2.3 on 2023-09-11 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balls',
            name='product',
        ),
        migrations.RemoveField(
            model_name='postcard',
            name='product',
        ),
        migrations.AddField(
            model_name='balls',
            name='product',
            field=models.ManyToManyField(to='product.product'),
        ),
        migrations.AddField(
            model_name='postcard',
            name='product',
            field=models.ManyToManyField(to='product.product'),
        ),
    ]
