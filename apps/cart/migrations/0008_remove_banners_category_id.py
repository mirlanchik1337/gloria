# Generated by Django 4.2.3 on 2023-08-19 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_alter_banners_category_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banners',
            name='category_id',
        ),
    ]
