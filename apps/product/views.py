from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import (Product, Category, Subcategory, Review)
from .serializers import (ProductSerializer, CategorySerializer, SubcategorySerializer, ReviewSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Product, Category, Subcategory, QuationsAnswers
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    SubcategorySerializer,
    QuationsAnswersSerializer,
)


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_slug'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', 'description']


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'category_slug'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', ]


class SubcategoryViewSet(ReadOnlyModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    lookup_field = 'subcategory_slug'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = IsAuthenticated,


class QuationsAnswersViewSet(ReadOnlyModelViewSet):
    queryset = QuationsAnswers.objects.all()
    serializer_class = QuationsAnswersSerializer
