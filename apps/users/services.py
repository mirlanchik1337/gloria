from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin


class PostOnlyViewSet(CreateModelMixin, viewsets.GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "METHOD NOT ALLOWED"})

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "METHOD NOT ALLOWED"})

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "METHOD NOT ALLOWED"})

    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "METHOD NOT ALLOWED"})

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "METHOD NOT ALLOWED"})


class GetLoginResponseService:
    @staticmethod
    def get_jwt(user):
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return data
