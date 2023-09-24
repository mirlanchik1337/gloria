from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CartItem, FavoriteProduct, Banners, Order, Filial
from apps.cart import serializers
from apps.cart.permissions import IsOwnerOrReadOnly
from ..product.models import Product, Transport, PostCardPrice, FontSize
from ..product.permissions import IsOwner
from ..cart import services

class CartItemListView(services.CartItemListViewService):
    queryset = CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        if product_id is None:
            return Response({"detail": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item_data = {
            "product": product.id,
            "user": request.user.id,
            "quantity": 1  # You might want to adjust this default value
        }

        serializer = self.get_serializer(data=cart_item_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FavoriteItemListView(services.FavoriteItemListService):
    queryset = FavoriteProduct.objects.all()
    serializer_class = serializers.FavoriteSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]


class FavoriteItemDetailView(services.FavoriteItemDetailViewService):
    queryset = FavoriteProduct.objects.all()
    serializer_class = serializers.FavoriteSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'


class BannersViewSet(generics.ListAPIView):
    queryset = Banners.objects.all()
    serializer_class = serializers.BannerSerializer


class OrderApiView(services.OrderApiService):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'


class OrderDetailApiView(services.OrderDetailServiceApiView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'

class OrderHistoryApiView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class HistoryOrderApiView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class TransportListView(generics.ListAPIView):
    queryset = Transport.objects.all()
    serializer_class = serializers.TransportSerializer


class PricePostCardView(generics.ListAPIView):
    queryset = PostCardPrice.objects.all()
    serializer_class = serializers.PricePostCardSerializer


class FilialView(generics.ListAPIView):
    queryset = Filial.objects.all()
    serializer_class = serializers.FilialSerializer


class FontSizeView(generics.ListAPIView):
    queryset = FontSize.objects.all()
    serializer_class = serializers.FontSizeSerializer
