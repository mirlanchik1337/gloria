from rest_framework import serializers
from rest_framework import serializers
from .models import FavoriteProduct
from apps.cart.models import CartItem
from ..product.serializers import ProductSerializer
from apps.product.models import Product


class CartProductSerializer(serializers.ModelSerializer):
    product = Product.objects.all()

    class Meta:
        model = Product
        fields = 'id name'.split()


class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # product = CartProductSerializer()
    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = CartProductSerializer(data={'name'})

    class Meta:
        model = CartItem
        fields = "user id quantity created_at product".split()


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavoriteProduct
        fields = '__all__'
