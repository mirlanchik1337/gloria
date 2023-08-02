from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a username.")
        user = self.model(
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_active', False)
        return self._create_user(
            phone_number, password, **extra_fields
        )

    def create_superuser(self, phone_number, password):
        return self._create_user(
            phone_number,
            password,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
