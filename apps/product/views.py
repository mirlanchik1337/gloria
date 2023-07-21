from rest_framework.viewsets import ModelViewSet
from .models import (Product, Category, Subcategory)
from .serializers import (ProductSerializer, CategorySerializer, SubcategorySerializer)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

