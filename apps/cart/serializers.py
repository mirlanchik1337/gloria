from rest_framework import serializers
from rest_framework import serializers
from .models import FavoriteProduct
from apps.cart.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = '__all__'
