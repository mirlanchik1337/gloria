# Generated by Django 4.2.3 on 2023-08-23 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_category_parent_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_category',
        ),
    ]
