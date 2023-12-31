from datetime import datetime, timedelta
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.product import filters as filtration
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from apps.product.models import (Product, Category,
                                 Subcategory, QuationsAnswers,
                                 Review, Stories,
                                 WhatsAppLink, SecondSubcategory,
                                 PostCard, Balls)
from apps.product.serializers import (
    ProductSerializer,
    CategorySerializer,
    SubcategorySerializer,
    QuationsAnswersSerializer,
    ReviewSerializer,
    StoriesSerializer,
    WhatsAppLinkSerializer,
    SecondSubcategorySerializer,
    PostCardSerializer,
    BalloonsSerializer)
from apps.product.pagination import CustomProductPagination, ProductLimitOffsetPagination
from .permissions import IsOwner
from ..cart.models import CartItem
from ..cart.permissions import IsOwnerOrReadOnly


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = filtration.ProductFilters
    filterset_fields = [
        'name', 'category',
        'subcategory', 'price',
        'quantity']
    search_fields = ['name', 'description']
    ordering = ['id']
    ordering_fields = ['price']
    pagination_class = ProductLimitOffsetPagination




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


class SecondSubcategoryViewSet(ReadOnlyModelViewSet):
    queryset = SecondSubcategory.objects.all()
    serializer_class = SecondSubcategorySerializer
    lookup_field = 'second_subcategory_slug'
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


class PostCardViewSet(ModelViewSet):
    queryset = PostCard.objects.all()
    serializer_class = PostCardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TitleOnBallViewSet(viewsets.ModelViewSet):
    serializer_class = BalloonsSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Используйте свой IsOwnerOrReadOnly класс

    def get_queryset(self):
        return Balls.objects.filter(user=self.request.user)

    def get(self):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    def create(self, request , *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)