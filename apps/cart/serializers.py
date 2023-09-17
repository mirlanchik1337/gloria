from rest_framework import serializers
from .models import FavoriteProduct, Order, Filial
from apps.cart.models import CartItem, Banners
from ..product.models import Transport, PostCardPrice, FontSize
from ..product.serializers import ProductImageSerializer


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

    def get_extra_price(self, obj):
        extra_price = 0

        # Учитываем цену открыток, если они есть
        if obj.product and hasattr(obj.product, 'postcard_set'):
            for postcard in obj.product.postcard_set.all():
                postcard_price = postcard.price.price * obj.quantity  # Use the price attribute of PostCardPrice
                extra_price += postcard_price

        # Учитываем цену шаров, если они есть
        if obj.product and hasattr(obj.product, 'balls_set'):
            for balls in obj.product.balls_set.all():
                balls_price = balls.size.price * obj.quantity  # Use the price attribute of PostCardPrice
                extra_price += balls_price
        return extra_price

    def get_total_price(self, obj):
        total_price = 0

        # Calculate total price based on the selected product
        if obj.product:
            total_price += obj.product.price * obj.quantity
        elif obj.postcard:
            total_price += obj.postcard.price * obj.quantity
        elif obj.balls:
            total_price += obj.balls.price * obj.quantity

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


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_items = CartItemSerializer(many=True, source='cartitem_set', read_only=True)
    price = CartItemSerializer(read_only=True, source='cart_items.product.price')
    order = OrderCartSerializer(read_only=True, source='cart_item.order')
    total_cart_price = serializers.SerializerMethodField()
    postcard = serializers.SerializerMethodField(read_only=True, source='cart.postcard')
    extra_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        ref_name = 'ProductOrder'

    def get_extra_price(self):
        extra_price = 0
        for cart_item in self.instance.cartitem_set.all():
            extra_price += cart_item.postcard.price * len(cart_item.postcard)
        return extra_price

    def get_total_cart_price(self, obj):
        total_price = 0
        for cart_item in obj.cartitem_set.all():
            total_price += cart_item.product.price * cart_item.quantity
        return total_price

    def get_postcard(self, order):
        # Ваш код для получения почтовых карт, связанных с данным заказом
        # Например, если у заказа есть поле postcards, вы можете вернуть их так:
        return PricePostCardSerializer(order.postcard.price, many=True).data


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = '__all__'


class PricePostCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCardPrice
        fields = '__all__'


class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = '__all__'


class FontSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FontSize
        fields = '__all__'
