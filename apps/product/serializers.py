from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import (Product, Category, Subcategory,
                     QuationsAnswers, Review, Stories,
                     WhatsAppLink, SecondSubcategory,
                     PostCard, PostCardPrice,
                     TitleOnBall, ImageModel, Order, TypeOfOrder, Filial)


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


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    categories = CategorySerializer(many=False)
    subcategories = SubcategorySerializer(many=False)
    second_subcategories = SecondSubcategorySerializer(many=False)
    product_images = ProductImageSerializer(many=True, read_only=True)

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


class PostCardPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCardPrice
        fields = '__all__'


class PostCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # product = ProductSerializer()
    class Meta:
        model = PostCard
        fields = ['id', 'user', 'text', 'price', 'product']


class TitleOnBallSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TitleOnBall
        fields = ['id', 'user', 'text', 'size', 'product']


class FilialSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, read_only=True)
    address = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = Filial
        fields = '__all__'

#
# class TypeOfOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TypeOfOrder
#         fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    filial = FilialSerializer()
    # type_of_order = TypeOfOrderSerializer()

    class Meta:
        model = Order
        fields = '__all__'
