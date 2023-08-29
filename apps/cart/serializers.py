from rest_framework import serializers
from rest_framework import serializers
from .models import FavoriteProduct
from apps.cart.models import CartItem, Banners
from ..product.models import ImageModel
from ..product.serializers import ProductSerializer, ProductImageSerializer
from .constants import base_url, urls_media
from apps.product.serializers import CategorySerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, source='product.product_images', read_only=True)
    price = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    is_hit = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    id = serializers.ReadOnlyField(source='product.pk')  # Используйте ReadOnlyField для id

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_price(self, obj):
        return obj.product.price * obj.quantity

    def get_product_slug(self, obj):
        return obj.product.product_slug

    def get_description(self, obj):
        return obj.product.description

    def get_is_hit(self, obj):
        return obj.product.is_hit

    def get_categories(self, obj):
        return obj.product.categories.id

    def get_subcategories(self, obj):
        return obj.product.subcategories.id

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_representation = {
            'id': instance.product.id,
            'name': instance.product.name,
            'price': instance.product.price,
            'product_slug': instance.product.product_slug,
            'description': instance.product.description,
            'is_hit': instance.product.is_hit,
            'categories': instance.product.categories.id,
            'subcategories': instance.product.subcategories.id,
        }
        representation.update(product_representation)
        return representation

class FavoriteSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, source='product.product_images', read_only=True)

    class Meta:
        model = FavoriteProduct
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_representation = {
            'name': instance.product.name,
            'price': instance.product.price,
            'product_slug': instance.product.product_slug,
            'description': instance.product.description,
            'is_hit': instance.product.is_hit,
            'quantity': instance.product.quantity,
        }
        representation.update(product_representation)
        return representation

    def create(self, validated_data):
        user = self.context['request'].user
        favorite, created = FavoriteProduct.objects.get_or_create(
            user=user,
            product=validated_data['product']
        )
        return favorite


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = '__all__'
