from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CartItem, FavoriteProduct, Banners, Order
from .serializers import CartItemSerializer, FavoriteSerializer, BannerSerializer, OrderSerializer
from apps.cart.permissions import IsOwnerOrReadOnly
from ..product.permissions import IsOwner
from ..cart import services


class CartItemListView(services.CartItemListViewService):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class CartItemDetailView(services.CartItemDetailViewService):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]


class FavoriteItemListView(services.FavoriteItemListService):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'product_id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]


class FavoriteItemDetailView(services.FavoriteItemDetailViewService):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'


class BannersViewSet(generics.ListAPIView):
    queryset = Banners.objects.all()
    serializer_class = BannerSerializer


class OrderApiView(services.OrderApiService):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'


class OrderDetailApiView(services.OrderDetailServiceApiView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
