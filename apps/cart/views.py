from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, FavoriteProduct
from .serializers import CartItemSerializer, FavoriteSerializer, CartSerializer


class CartItemCreateView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartItemListView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['product__name', ]

    def delete(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        cart_items.delete()
        return Response(
            {"message": "Корзина была успешно очищена."}, status=status.HTTP_200_OK
        )


class CartItemDetailView(generics.RetrieveDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class FavoriteCreateView(generics.CreateAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = IsAuthenticated,

    def delete(self, request, *args, **kwargs):
        favorite_items = self.get_queryset()
        favorite_items.delete()
        return Response(
            {"message": "Избранные были успешно очищены."}, status=status.HTTP_200_OK
        )
