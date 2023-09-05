from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from apps.cart.models import Order, CartItem, FavoriteProduct
from apps.cart.serializers import OrderSerializer, CartItemSerializer
from apps.product.models import Product


class OrderApiService(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        order = Order.objects.create(user=user, order_date_time=timezone.now())
        for cart_item in cart_items:
            order.cart_items.add(cart_item)
        if order.filial.name_address:
            order.filial_id = order.filial.name_address
        else:
            order.filial_id = 1
        order.save()
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_quantity(self):
        cart_items = CartItem.objects.all()
        product = Product.objects.get(id=self.kwargs.get('product_id'))
        quantity = product.quantity - cart_items.quantity
        product.quantity = quantity
        product.save()
        return quantity


class OrderDetailServiceApiView(generics.RetrieveDestroyAPIView):
    def list_order_detail(self, request):
        user = request.user
        order = Order.objects.filter(user=user)
        serializer = self.get_serializer(order, many=True)
        total_price = serializer.get_total_price(order.cart_items.total_price * order.cart_items.quantity)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FavoriteItemListService(generics.ListCreateAPIView):
    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)

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


class FavoriteItemDetailViewService(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)


class CartItemListViewService(generics.ListCreateAPIView):
    def list(self, request, *args, **kwargs):
        cart_items = CartItem.objects.all()

        # Include the total price in the response
        serializer = self.get_serializer(cart_items, many=True)
        response_data = {
            'cart_items': serializer.data,
        }
        return Response(response_data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

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


class CartItemDetailViewService(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

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

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        product_id = request.data.get('product_id')

        if product_id is not None:
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
            instance.product = product

        quantity = request.data.get('quantity')
        if quantity is not None:
            instance.quantity = quantity
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
