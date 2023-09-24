# Generated by Django 4.2.3 on 2023-09-24 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balls',
            name='balls_size',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='product.fontsize', verbose_name='Размер шрифта'),
        ),
        migrations.AlterField(
            model_name='balls',
            name='is_cart',
            field=models.BooleanField(default=False, verbose_name='Добавление надписи к шару'),
        ),
        migrations.AlterField(
            model_name='balls',
            name='price',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.ballsprice'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='balls',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postcard',
            name='price',
            field=models.ForeignKey(default=25, on_delete=django.db.models.deletion.CASCADE, to='product.postcardprice', verbose_name='Цена открытки'),
        ),
        migrations.AlterField(
            model_name='postcard',
            name='text',
            field=models.CharField(default=1, max_length=100, verbose_name='Текст на открытке для букетов'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
