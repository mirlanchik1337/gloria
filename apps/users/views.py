from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import hashers
from rest_framework import (
    status,
    viewsets,
    permissions,
    exceptions,
    response
)
from .services import PostOnlyViewSet, UserServices
from .models import User, UserCode
from .services import GetLoginResponseService
from .permissions import IsOwner
from . import serializers


class PasswordResetNewPasswordViewSet(PostOnlyViewSet):
    queryset = UserCode.objects.all()
    serializer_class = serializers.PasswordResetNewPasswordSerializer
    lookup_field = 'code'

    def create(self, request, *args, **kwargs):
        try:
            password_reset_token = UserCode.objects.get(
                code=request.data["code"], time__gt=timezone.now()
            )
        except UserCode.DoesNotExist:
            return {"detail": "Not Found"}

        user = password_reset_token.user

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["password"]

        # Установка нового хэшированного пароля для пользователя
        user.set_password(password)
        user.save()

        password_reset_token.delete()  # Удаление токена

        return {"message": "success"}

class PasswordResetTokenViewSet(PostOnlyViewSet):
    """API для введения кода"""

    serializer_class = serializers.PasswordResetTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                password_reset_token_service = UserServices.user_password_reset_token_service(serializer)
                return response.Response(
                    data={"detail": password_reset_token_service},
                    status=status.HTTP_200_OK)

            except UserCode.DoesNotExist:
                return response.Response(
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                    data={"error": "Not Found"})


class PasswordResetSearchUserViewSet(PostOnlyViewSet):
    """API для поиска user и создание кода"""

    serializer_class = serializers.PasswordResetSearchUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        code = UserServices.user_password_reset_search_user_service(serializer)
        if code:
            return response.Response(
                data={"message": "sended", "code": code},
                status=status.HTTP_200_OK,
            )


class UserRegistrationViewSet(PostOnlyViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            register = UserServices.user_registration_service(serializer)
            return response.Response(data={
                "message": "Sended",
                "detail": register})

        except IntegrityError:
            return response.Response(
                data={"detail": "Already Exist"},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserConfirmViewSet(PostOnlyViewSet):
    serializer_class = serializers.UserConfimSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            confirm = UserServices.user_confirm_service(serializer)
            return response.Response(data=confirm)

        except ValueError:
            return response.Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"error": "write code number"},
            )


class UserLoginViewSet(PostOnlyViewSet):
    serializer_class = serializers.UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request=request, **serializer.validated_data)

        if not user:
            raise exceptions.AuthenticationFailed
        login(request, user)
        return response.Response(
            data={"id": user.id,
                  "detail": GetLoginResponseService.get_jwt(user=user)
                  }
        )


class LogoutViewSet(PostOnlyViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logout(request)
        return response.Response({"message": "success"})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def list(self):
        user = self.request.user
        queryset = User.objects.filter(id=user.id)
        return queryset


class ProfileDetailAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'


class SetPasswordViewSet(PostOnlyViewSet):
    serializer_class = serializers.SetPasswordSerilizer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        user = request.user.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        try:
            user = User.objects.get(id=user)
            user.password = hashers.make_password(new_password)
            user.save()
            return response.Response(data={"message": "success"})
        except User.DoesNotExist:
            return response.Response(
                data={"message": "Wrong"})
