from jsonschema.exceptions import ValidationError
from rest_framework import serializers
from .models import User


class PasswordResetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={"input_type": "password"}, help_text="min length 4", min_length=4
    )


class PasswordResetTokenSerializer(serializers.Serializer):
    code = serializers.CharField()


class PasswordResetSearchUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, phone_number):
        try:
            User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return ValidationError(
                f"Пользователь с указанным номеров телефона не найден."
            )
        return phone_number


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "fullname",
            "phone_number",
        )


class UserRegistrationSerializer(serializers.Serializer):
    fullname = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(
        style={"input_type": "password"}, help_text="min length 4", min_length=4
    )


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(
        style={"input_type": "password"}, help_text="min length 4", min_length=4
    )


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class UserConfimSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
