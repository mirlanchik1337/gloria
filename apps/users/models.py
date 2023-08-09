from django.db import models
from .validators import PhoneValidator
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .choices import GENDER_CHOICES


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField("Фио", max_length=100)
    phone_number = models.CharField(
        "Телефон", validators=[PhoneValidator], unique=True, max_length=300
    )
    date_of_birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
    avatar = models.ImageField(null=True, upload_to='avatars/', blank=True)
    is_active = models.BooleanField("Активен", default=False)
    is_staff = models.BooleanField("Персонал", default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []  # Необязательные поля для создания суперпользователя

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.fullname}, {self.phone_number}"


class UserConfirm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users_code')
    code = models.CharField(max_length=6)

    class Meta:
        verbose_name = "Код Верификации"
        verbose_name_plural = "Коды Верификации"

    def __str__(self):
        return f"{self.user}, {self.code}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    time = models.DateTimeField()

    class Meta:
        verbose_name = "Сброс пароля"
        verbose_name_plural = "Сбросы паролей"

    def __str__(self):
        return f"{self.user}, {self.token}"
