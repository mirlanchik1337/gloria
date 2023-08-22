from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, FavoriteProduct, Banners
from .serializers import CartItemSerializer, FavoriteSerializer, BannerSerializer
from apps.cart.permissions import IsOwnerOrReadOnly
from ..product.models import Product


class CartItemListView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Delete all objects
        CartItem.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        user = request.user

        # Check if the product already exists in the cart
        existing_item = CartItem.objects.filter(product_id=product_id, user=user).first()

        if existing_item:
            # If the product is already in the cart, just increase the quantity
            existing_item.quantity += 1
            existing_item.save()
            serializer = CartItemSerializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If the product is not in the cart, create a new item
            serializer = CartItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        if product_id is None:
            return Response({"detail": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item_data = {
            "product": product.id,
            "user": request.user.id,
            "quantity": 1  # You might want to adjust this default value
        }

        serializer = self.get_serializer(data=cart_item_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FavoriteItemListView(generics.ListCreateAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        user = request.user  # Assuming you have implemented user authentication

        # Check if the product is already in the user's favorites
        if FavoriteProduct.objects.filter(user=user, product_id=product_id).exists():
            return Response({"detail": "Product is already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)  # Save the favorite with the user reference
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        # Delete all favorite objects
        FavoriteProduct.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated, ]


class BannersViewSet(generics.ListAPIView):
    queryset = Banners.objects.all()
    serializer_class = BannerSerializer
