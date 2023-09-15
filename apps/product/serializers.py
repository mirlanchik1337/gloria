from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import (Product, Category, Subcategory,
                     QuationsAnswers, Review, Stories,
                     WhatsAppLink, SecondSubcategory,
                     PostCard, PostCardPrice,
                     Balls, ImageModel)
from ..cart.models import CartItem , Order


class SubcategoryForCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    subcategories = SubcategoryForCategorySerializer(many=True, source='subcategory_set')

    class Meta:
        model = Category
        fields = "__all__"


class SecondSubcategoryForSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondSubcategory
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=False)
    second_subcategories = SecondSubcategoryForSubcategorySerializer(many=True, source='secondsubcategory_set')

    class Meta:
        model = Subcategory
        fields = "__all__"


class SecondSubcategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=False)
    subcategories = SubcategorySerializer(many=False)

    class Meta:
        model = SecondSubcategory
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = "id image".split()


class PostCardPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCardPrice
        fields = '__all__'


class PostCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PostCard
        fields = ['id', 'user', 'text', 'price']


class BalloonsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Balls
        fields = ['id', 'user', 'text', 'size']


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    categories = CategorySerializer(many=False)
    subcategories = SubcategorySerializer(many=False)
    second_subcategories = SecondSubcategorySerializer(many=False)
    product_images = ProductImageSerializer(many=True, read_only=True)
    postcard = PostCardSerializer(many=False, read_only=True)
    baloons = BalloonsSerializer(many=False , read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'


class QuationsAnswersSerializer(ModelSerializer):
    class Meta:
        model = QuationsAnswers
        fields = "__all__"


class StoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = '__all__'


class WhatsAppLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppLink
        fields = '__all__'


class CartItemForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


