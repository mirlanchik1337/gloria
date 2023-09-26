from django.db.models import Sum
from rest_framework import serializers

from . import models
from .models import FavoriteProduct, Order, Filial
from apps.cart.models import CartItem, Banners
from ..product.models import Transport, PostCardPrice, FontSize
from ..product.serializers import ProductImageSerializer
from ..product.serializers import BalloonsSerializer, PostCardSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, source='product.product_images', read_only=True)
    price = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    is_hit = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    product_quantity = serializers.SerializerMethodField()
    extra_price = serializers.SerializerMethodField()
    postcard = PostCardSerializer(many=True, read_only=True)
    balls = BalloonsSerializer(many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"


    def get_price(self, obj):
        if obj.product:
            return obj.product.price

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

    def get_extra_price(self, obj):
        extra_price = 0

        # Check if obj.product has postcards and calculate the price based on user-specific information
        if obj.product and hasattr(obj.product, 'postcard_set'):
            for postcard in obj.product.postcard_set.all():
                # Check if postcard has a price and price.price attribute before using it
                if hasattr(postcard, 'price') and hasattr(postcard.price, 'price'):
                    postcard_price = postcard.price.price
                    extra_price += postcard_price

        return extra_price

    def update(self, instance, validated_data):
        available_quantity = instance.product.product_quantity if instance.product else 0
        new_quantity = validated_data.get('quantity', instance.quantity)
        if new_quantity > available_quantity:
            new_quantity = available_quantity
        instance.quantity = new_quantity
        instance.save()

        return instance

    def get_total_price(self, obj):
        total_price = 0

        # Calculate total price based on the selected product
        if obj.product:
            total_price += obj.product.price * obj.quantity
        elif obj.product.postcard_set:
            total_price += obj.product.postcard_set.price
        elif obj.balls:
            total_price += obj.product.balls_set.price * obj.quantity

        # Add the extra price to the total price
        total_price += self.get_extra_price(obj)

        return total_price

    def get_product_quantity(self, obj):
        return obj.product.product_quantity

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cart_representation = {
            'id': instance.id if instance.id else None,
            'name': instance.product.name if instance.product else None,
            'price': instance.product.price if instance.product else None,
            'product_slug': instance.product.product_slug if instance.product else None,
            'description': instance.product.description if instance.product else None,
            'is_hit': instance.product.is_hit if instance.product else None,
            'categories': instance.product.categories.id if instance.product and instance.product.categories else None,
            'subcategories': instance.product.subcategories.id if instance.product and instance.product.subcategories else None,
            'product_quantity': instance.product.product_quantity if instance.product else None,
            'balls': [
                BalloonsSerializer(instance.product.balls_set.all(),
                                   many=True).data if instance.product.balls_set else None,
            ],
            'postcard': PostCardSerializer(instance.product.postcard_set.all(),
                                           many=True).data if instance.product.postcard_set.exists() else None,
        }
        representation.update(cart_representation)
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
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Banners
        fields = '__all__'

    def get_category_name(self, obj):
        return f"{obj.category.name}"


class CartOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = '__all__'


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = '__all__'


class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_items = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    order = OrderCartSerializer(read_only=True, source='cart.cartitem_set.order')
    postcard = PostCardSerializer(many=True, read_only=True)
    balls = BalloonsSerializer(many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField()
    transport = TransportSerializer(many=False, read_only=True)
    filial = FilialSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        ref_name = 'ProductOrder'

    def get_cart_items(self, obj):
        # Assuming you want to serialize the cart items
        cart_items = obj.cartitem_set.all()
        cart_items = tuple(cart_items)
        return CartItemSerializer(cart_items, many=True).data

    def get_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.cartitem_set.all())

    def get_total_cart_price(self, obj):
        total_price = self.get_price(obj)
        total_price += int(obj.transport.price)
        return total_price


class PricePostCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCardPrice
        fields = '__all__'


class FontSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FontSize
        fields = '__all__'
