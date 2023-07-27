from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, FavoriteProduct
from .serializers import CartItemSerializer, FavoriteSerializer


class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

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
