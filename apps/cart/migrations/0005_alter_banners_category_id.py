# Generated by Django 4.2.3 on 2023-08-17 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_banners_category_id_alter_banners_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='category_id',
            field=models.CharField(max_length=700, verbose_name='<property object at 0x0000016AFABE1E90>'),
        ),
    ]
