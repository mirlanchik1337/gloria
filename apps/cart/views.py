from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, FavoriteProduct, Banners
from .serializers import CartItemSerializer, FavoriteSerializer, BannerSerializer


class CartItemListSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['product__name', ]

    def destroy(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            try:
                cart_item = self.get_queryset().get(pk=kwargs['pk'])
                cart_item.delete()
                return Response(
                    {"message": "Товар был успешно удален из корзины."},
                    status=status.HTTP_204_NO_CONTENT
                )
            except CartItem.DoesNotExist:
                return Response(
                    {"message": "Товар не найден в корзине."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            cart_items = self.get_queryset()
            cart_items.delete()
            return Response(
                {"message": "Корзина была успешно очищена."},
                status=status.HTTP_200_OK
            )


class FavoriteCreateSet(viewsets.ModelViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def destroy(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            try:
                cart_item = self.get_queryset().get(pk=kwargs['pk'])
                cart_item.delete()
                return Response(
                    {"message": " Избранный товар был успешно удален из корзины."},
                    status=status.HTTP_204_NO_CONTENT
                )
            except FavoriteProduct.DoesNotExist:
                return Response(
                    {"message": "Избранный товар не найден в корзине."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            favorite_items = self.get_queryset()
            favorite_items.delete()
            return Response(
                {"message": "Избранные были успешно очищена."},
                status=status.HTTP_200_OK
            )


class BannersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banners.objects.all()
    serializer_class = BannerSerializer
