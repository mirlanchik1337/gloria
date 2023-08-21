from rest_framework import serializers
from rest_framework import serializers
from .models import FavoriteProduct
from apps.cart.models import CartItem, Banners
from ..product.models import ImageModel
from ..product.serializers import ProductSerializer, ProductImageSerializer
from .constants import base_url, urls_media



class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_price(self, obj):
        return obj.product.price * obj.quantity


    def get_id(self, obj):
        return obj.id


class FavoriteSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    product_images = ProductImageSerializer(many=True, source='product.product_images', read_only=True)
    product_slug = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    is_hit = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    class Meta:
        model = FavoriteProduct
        fields = '__all__'

    def get_image(self, obj):
        return f'{obj.product.imag}'

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

    def get_quantity(self, obj):
        return obj.product.quantity
    def create(self, validated_data):
        user = self.context['request'].user  # Get the user from the request
        favorite, created = FavoriteProduct.objects.get_or_create(
            user=user,
            product=validated_data['product']  # Use the product field from the validated_data
        )
        return favorite

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = '__all__'
