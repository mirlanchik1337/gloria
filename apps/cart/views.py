from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, Product
from .serializers import CartItemSerializer


class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartItemDetailView(generics.RetrieveUpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
