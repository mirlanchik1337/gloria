from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import hashers
from rest_framework import (
    status,
    viewsets,
    permissions,
    exceptions,
    response,
    views
)
from .services import PostOnlyViewSet, UserServices
from .models import User, UserCode
from .services import GetLoginResponseService
from .permissions import IsOwner
from . import serializers


class PasswordResetNewPasswordViewSet(views.APIView):
    serializer_class = serializers.PasswordResetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        new_password_service = UserServices.user_password_reset_new_password(serializer)
        return response.Response(data=new_password_service)


class PasswordResetTokenViewSet(PostOnlyViewSet):
    """API для введения кода"""

    serializer_class = serializers.PasswordResetTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password_reset_token_service = UserServices.user_password_reset_token_service(serializer)
            return response.Response(
                data=password_reset_token_service,
                status=status.HTTP_200_OK)


class PasswordResetSearchUserViewSet(PostOnlyViewSet):
    serializer_class = serializers.PasswordResetSearchUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        code = UserServices.user_password_reset_search_user_service(serializer)
        if code:
            return response.Response(
                data=code,
                status=status.HTTP_200_OK)


class UserRegistrationViewSet(PostOnlyViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            register = UserServices.user_registration_service(serializer)
            return response.Response(data=register)

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
