# Generated by Django 4.2.3 on 2023-09-14 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_postcard_text'),
        ('cart', '0005_alter_order_transport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banners',
            name='link',
        ),
        migrations.AddField(
            model_name='banners',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.category'),
            preserve_default=False,
        ),
    ]
