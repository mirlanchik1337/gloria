from rest_framework.serializers import ModelSerializer
from .models import Product, Category, Subcategory, QuationsAnswers


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubcategorySerializer(ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class QuationsAnswersSerializer(ModelSerializer):
    class Meta:
        model = QuationsAnswers
        fields = "__all__"
