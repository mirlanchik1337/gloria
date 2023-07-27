from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product, Category, Subcategory, QuationsAnswers,  Review




class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(min_value=1)
    categories = CategorySerializer(many=False)

    class Meta:
        model = Product
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class QuationsAnswersSerializer(ModelSerializer):
    class Meta:
        model = QuationsAnswers
        fields = "__all__"

