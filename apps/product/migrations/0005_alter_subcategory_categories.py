# Generated by Django 4.2.3 on 2023-08-23 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_subcategory_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='categories',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Категория'),
        ),
    ]
