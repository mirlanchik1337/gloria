from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from . import models


class Service:
    model = None

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return cls.model.objects.get(*args, **kwargs)
        except cls.model.DoesNotExist:
            raise ValueError('Model have to be instant')

    @classmethod
    def filter(cls, *args, **kwargs):
        try:
            return cls.model.objects.filter(*args, **kwargs).order_by('-created_at')
        except cls.model.DoesNotExist:
            raise ValueError('Model have to be instant')


class ConfirmCodeService(Service):
    model = models.UserConfirm


class ResetTokenService(Service):
    model = models.PasswordResetToken


class UserService(Service):
    model = models.User

    @staticmethod
    def get_token(user):
        refresh = RefreshToken.for_user(user)
        token = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return token

    @classmethod
    def check_code(cls, code):
        if ConfirmCodeService.filter(code=code):
            cls.model.objects.update(is_active=True)
            ConfirmCodeService.filter(code=code).delete()
            return True
        else:
            return False


class GetLoginResponseService:
    @staticmethod
    def get_login_response(user, request):
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        print(refresh)
        return data
