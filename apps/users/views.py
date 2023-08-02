from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout, hashers
from django.utils import timezone
from rest_framework import (
    status,
    generics,
    permissions,
    views,
    exceptions,
    response,
)

from .models import User, PasswordResetToken, UserConfirm
from . import serializers, utils
from .services import GetLoginResponseService

class PasswordResetNewPasswordAPIView(generics.CreateAPIView):
    """API для сброса пароля"""

    serializer_class = serializers.PasswordResetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            password_reset_token = PasswordResetToken.objects.get(
                token=kwargs["code"], time__gt=timezone.now()
            )
        except PasswordResetToken.DoesNotExist:
            return response.Response(
                data={
                    "detail": f"Недействительный токен для сброса пароля или время истечения токена закончилось.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.is_valid(raise_exception=True)
        # Обновление пароля пользователя
        user = password_reset_token.user
        password = serializer.validated_data["password"]
        user.password = hashers.make_password(password)
        user.save()

        password_reset_token.delete()  # Удаление токена

        return response.Response(
            data={"detail": "Пароль успешно сброшен."}, status=status.HTTP_200_OK
        )


class PasswordResetTokenAPIView(generics.CreateAPIView):
    """API для введения токена"""

    serializer_class = serializers.PasswordResetTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                code = serializer.validated_data["code"]
                reset_code = PasswordResetToken.objects.get(
                    token=code, time__gt=timezone.now()
                )
            except Exception as e:
                return response.Response(
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                    data={
                        "error": f"Недействительный код для сброса пароля или время истечения токена закончилось"},
                )
            return response.Response(
                data={"detail": "ok", "code": f"{code}"}, status=status.HTTP_200_OK)


class PasswordResetSearchUserAPIView(generics.CreateAPIView):
    """API для поиска user и создание кода"""

    serializer_class = serializers.PasswordResetSearchUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                phone_number = serializer.validated_data["phone_number"]
                user = User.objects.get(phone_number=phone_number)
            except:
                return response.Response(
                    data={
                        "error": "Пользователь с указанным номеров телефона не найден."
                    }
                )
            # Генерация токена для сброса type(п)
            code = utils.generate_verification_code()
            time = timezone.now() + timezone.timedelta(minutes=5)

            # Сохранение токена в базе данных
            password_reset_token = PasswordResetToken(user=user, token=code, time=time)
            password_reset_token.save()
            # utils.send_to_the_code_phone(phone_number, code)
            print(code)

            return response.Response(
                data={"detail": "Сообщение отправлено вам на номер телефона!", "code": f"{code}"},
                status=status.HTTP_200_OK,
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**serializer.validated_data)
            activate_code = utils.generate_verification_code()
            code = UserConfirm.objects.create(user_id=user.id, code=activate_code)
            utils.send_to_the_code_phone(
                serializer.validated_data["phone_number"], activate_code
            )
            return response.Response(
                data={
                    "detail": f"Код для подтверждения пользователя отправлен вам на номер телефона {user.phone_number}"
                }
            )
        except IntegrityError:
            return response.Response(
                data={"detail": "Пользователь с данным номером телефона существует!"}
            )


class UserConfirmAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserConfimSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            if UserConfirm.objects.filter(code=serializer.validated_data["code"]):
                User.objects.update(is_active=True)
                UserConfirm.objects.filter(
                    code=serializer.validated_data["code"]
                ).delete()
                return response.Response(
                    status=status.HTTP_202_ACCEPTED, data={"success": "confirmed"}
                )

            return response.Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"error": "wrong id or code!"},
            )

        except ValueError:
            return response.Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"error": "write code number!"},
            )


class UserLoginUserAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request=request, phone_number=serializer.validated_data.get("phone_number"),
                            password=serializer.validated_data.get("password"))

        if not user:
            raise exceptions.AuthenticationFailed
        login(request, user)
        return response.Response(
            data=GetLoginResponseService.get_login_response(user, request)
        )


class LogoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logout(request)
        return response.Response({"detail": "Вы успешно вышли из системы."})


class ProfileAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(id=user.id)
        return queryset


class ProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    lookup_field = 'id'
