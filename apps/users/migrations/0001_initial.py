# Generated by Django 4.2.3 on 2023-08-29 06:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('fullname', models.CharField(max_length=40, verbose_name='Имя')),
                ('phone_number', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(regex='^996(\\d{3})\\d{2}\\d{2}\\d{2}$')], verbose_name='Телефон')),
                ('password', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=40, null=True)),
                ('date_of_birthday', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[(1, 'Мужской'), (2, 'Женский')], max_length=20, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активен')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Персонал')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('time', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Код Верификации',
                'verbose_name_plural': 'Коды Верификации',
            },
        ),
    ]
