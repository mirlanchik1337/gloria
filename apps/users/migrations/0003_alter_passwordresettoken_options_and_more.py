# Generated by Django 4.2.3 on 2023-08-09 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar_user_date_of_birthday_user_gender'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passwordresettoken',
            options={'verbose_name': 'Сброс пароля', 'verbose_name_plural': 'Сбросы паролей'},
        ),
        migrations.AlterModelOptions(
            name='userconfirm',
            options={'verbose_name': 'Код Верификации', 'verbose_name_plural': 'Коды Верификации'},
        ),
    ]
