# Generated by Django 4.2.3 on 2023-08-19 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_banners_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='category_id',
            field=models.CharField(max_length=700, verbose_name='<property object at 0x00000293F8141E90>'),
        ),
    ]
