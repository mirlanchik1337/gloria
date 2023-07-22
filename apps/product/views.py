from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import (Product, Category, Subcategory)
from .serializers import (ProductSerializer, CategorySerializer, SubcategorySerializer)


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(ReadOnlyModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

