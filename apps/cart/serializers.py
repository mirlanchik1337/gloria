from rest_framework import serializers
from rest_framework import serializers
from .models import FavoriteProduct
from apps.cart.models import CartItem
from ..product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = "__all__"
    def get_price(self, obj):
        return obj.product.price * obj.quantity

class FavoriteSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteProduct
        fields = '__all__'

    def get_price(self, obj):
        return obj.product.price