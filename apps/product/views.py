from rest_framework.permissions import IsAuthenticated
from apps.product import filters as filtration
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Product, Category, Subcategory, QuationsAnswers, Review, Stories
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    SubcategorySerializer,
    QuationsAnswersSerializer,
    ReviewSerializer,
    StoriesSerializer
)
from apps.product.pagination import CustomProductPagination


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = filtration.ProductFilters
    filterset_fields = [
        'name', 'category', 'subcategory', 'price', 'quantity'
    ]
    search_fields = ['name']
    ordering_fields = ['price']
    pagination_class = CustomProductPagination



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
    pagination_class = CustomProductPagination


class StoriesViewSet(ReadOnlyModelViewSet):
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializer
