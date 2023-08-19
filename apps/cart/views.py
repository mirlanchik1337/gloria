from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, FavoriteProduct, Banners
from .serializers import CartItemSerializer, FavoriteSerializer, BannerSerializer


class CartItemListView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def delete(self, request, *args, **kwargs):
        # Delete all objects
        CartItem.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'id'


class FavoriteItemListView(generics.ListCreateAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        # Check if the product is already in favorites
        if FavoriteProduct.objects.filter(product_id=product_id).exists():
            return Response({"detail": "Product is already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        # If not, create a new favorite
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        # Delete all favorite objects
        FavoriteProduct.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'id'


class BannersViewSet(generics.ListAPIView):
    queryset = Banners.objects.all()
    serializer_class = BannerSerializer
