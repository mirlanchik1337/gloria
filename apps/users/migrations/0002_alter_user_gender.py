# Generated by Django 4.2.3 on 2023-09-04 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[(1, 'Мужской'), (2, 'Женский')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]