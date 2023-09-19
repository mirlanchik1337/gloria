from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .validators import PhoneValidator
from .managers import UserManager
from .choices import GENDER_CHOICES


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField("Имя", max_length=40)
    phone_number = models.CharField(
        "Телефон", validators=[PhoneValidator], unique=True, max_length=15
    )
    password = models.CharField(max_length=255)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    date_of_birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    avatar = models.ImageField(null=True, upload_to='avatars/', blank=True, default='static/static/logo/userlogo.png')
    is_active = models.BooleanField("Активен", default=False)
    is_staff = models.BooleanField("Персонал", default=False)

    def save(self, *args, **kwargs):
        self.username = self.fullname.strip().lower()
        super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.fullname}, {self.phone_number}"


class UserCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    time = models.DateTimeField()

    class Meta:
        verbose_name = "Код Верификации"
        verbose_name_plural = "Коды Верификации"

    def __str__(self):
        return f"{self.user}, {self.code}"
