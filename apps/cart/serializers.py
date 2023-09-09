from rest_framework import serializers
from .models import FavoriteProduct, Order
from apps.cart.models import CartItem, Banners
from ..product.serializers import ProductImageSerializer, OrderSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, source='product.product_images', read_only=True)
    price = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    is_hit = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_price(self, obj):
        if obj.product:
            return obj.product.price
        elif obj.postcard:
            return obj.postcard.price
        elif obj.balls:
            return obj.balls.price
        return 0

    def get_product_slug(self, obj):
        return obj.product.product_slug

    def get_description(self, obj):
        if obj.product:
            return obj.product.description

    def get_is_hit(self, obj):
        if obj.product:
            return obj.product.is_hit

    def get_categories(self, obj):
        if obj.product and obj.product.categories:
            return obj.product.categories.id

    def get_subcategories(self, obj):
        if obj.product and obj.product.subcategories:
            return obj.product.subcategories.id

    def get_total_price(self, obj):
        if obj.product:
            return obj.product.price * obj.quantity

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_representation = {
            'id': instance.product.id if instance.product else None,
            'name': instance.product.name if instance.product else None,
            'price': instance.product.price if instance.product else None,
            'product_slug': instance.product.product_slug if instance.product else None,
            'description': instance.product.description if instance.product else None,
            'is_hit': instance.product.is_hit if instance.product else None,
            'categories': instance.product.categories.id if instance.product and instance.product.categories else None,
            'subcategories': instance.product.subcategories.id if instance.product and instance.product.subcategories else None,
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


class CartOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_items = CartItemSerializer(many=True, source='cartitem_set', read_only=True)
    price = CartItemSerializer(read_only=True, source='cart_items.product.price')
    order = OrderSerializer(read_only=True, source='cart_item.order')
    total_cart_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_total_cart_price(self, obj):
        total_price = 0
        for cart_item in obj.cartitem_set.all():
            total_price += cart_item.product.price * cart_item.quantity
        return total_price
