from datetime import datetime, timedelta

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.product import filters as filtration
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Product, Category, Subcategory, QuationsAnswers, Review, Stories, WhatsAppLink
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    SubcategorySerializer,
    QuationsAnswersSerializer,
    ReviewSerializer,
    StoriesSerializer, WhatsAppLinkSerializer
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
    queryset = Stories.objects.all().order_by('-created_at')
    serializer_class = StoriesSerializer

    def delete_old_stories(self):
        time_threshold = datetime.now() - timedelta(hours=24)
        Stories.objects.filter(created_at__lt=time_threshold).delete()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WhatsAppLinkViewSet(ReadOnlyModelViewSet):
    queryset = WhatsAppLink.objects.all()
    serializer_class = WhatsAppLinkSerializer

    def list(self, request, *args, **kwargs):
        phone_number = '+996500243213'
        encoded_phone_number = phone_number.replace('+', '').replace(' ', '')
        whatsapp_url = f'https://api.whatsapp.com/send?phone={encoded_phone_number}'
        return Response({'whatsapp_url': whatsapp_url})
    