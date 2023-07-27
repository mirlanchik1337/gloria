from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, password, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a username.")
        user = self.model(
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password, phone_number, **extra_fields):
        return self._create_user(
            password, phone_number, is_active=False, **extra_fields
        )

    def create_superuser(self, phone_number, password):
        return self._create_user(
            password,
            phone_number,
            is_staff=True,
            is_superuser=True,
        )
