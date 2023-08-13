from rest_framework import serializers
from rest_framework import serializers
from .models import FavoriteProduct
from apps.cart.models import CartItem, Banners
from ..product.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_price(self, obj):
        return obj.product.price * obj.quantity


class FavoriteSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    is_hit = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteProduct
        fields = '__all__'

    def get_image(self, obj):
        return f'http://127.0.0.1:8000/media/{obj.product.image_1}'

    def get_price(self, obj):
        return obj.product.price

    def get_product_slug(self, obj):
        return obj.product.product_slug

    def get_description(self, obj):
        return obj.product.description

    def get_is_hit(self, obj):
        return obj.product.is_hit

    def get_name(self, obj):
        return obj.product.name


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = '__all__'
