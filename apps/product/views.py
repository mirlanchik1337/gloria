from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import (Product, Category, Subcategory, Review)
from .serializers import (ProductSerializer, CategorySerializer, SubcategorySerializer, ReviewSerializer)
from rest_framework.permissions import IsAuthenticated



class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer





class SubcategoryViewSet(ReadOnlyModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = IsAuthenticated


