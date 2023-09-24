from django.conf import settings
from django.db.models import Sum
from telegram import Bot
from django.db.models.signals import post_save
from django.dispatch import receiver
import asyncio
from apps.cart.models import Chat
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from apps.cart.models import Order, CartItem, FavoriteProduct
from apps.cart.serializers import OrderSerializer, CartItemSerializer
import requests
from django.db import transaction


def calculate_order_volume(cart_items):
    order_volume = 0

    for cart_item in cart_items:
        product_volume = cart_item.product.volume
        quantity = cart_item.quantity
        order_volume += product_volume * quantity

    return order_volume


class OrderApiService(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items:
            return Response({"error": "Корзина пуста. Создание заказа невозможно."},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            new_order = serializer.save()

            # Associate each cart item with the new order
            for cart_item in cart_items:
                cart_item.order = new_order
                cart_item.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailServiceApiView(generics.RetrieveDestroyAPIView):
    def list_order_detail(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        total_price = orders.aggregate(total_price=Sum('cartitem__price'))['total_price']

        return Response({"total_price": total_price, "details": serializer.data}, status=status.HTTP_200_OK)


class FavoriteItemListService(generics.ListCreateAPIView):
    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        user = request.user  # Assuming you have implemented user authentication
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
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        serializer = self.get_serializer(cart_items, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        cart_items.delete()
        return Response({"message": "All objects in the cart have been successfully deleted."})

    def create(self, request, *args, **kwargs):
        data = request.data
        quantity = int(data.get('quantity', 1))
        product = data.get('product')
        existing_item = CartItem.objects.filter(user=request.user, product=product).first()

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define the send_notification function (replace this with your actual notification logic)
def send_notification(message):
    # Replace this with your notification sending code (e.g., sending an email or a push notification)
    print(f"Sending notification: {message}")


@receiver(post_save, sender=Order, dispatch_uid="send_order_notification")
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        # Replace 'https://your-api-url.com/get_order_price' with the actual API URL
        api_url = 'http://127.0.0.1:8000/api/v1/orders/'

        try:
            response = requests.get(api_url, params={'order_id': instance.id})

            if response.status_code == 200:
                price_data = response.json()
                price = price_data.get('price')
            else:
                # Handle API error or price not found
                price = 'Price not available'
        except requests.exceptions.RequestException as e:
            # Handle request-related errors (e.g., network issues)
            price = 'Error fetching price from API'

        message = "Новый заказ!\n\n"
        message += f"Имя заказчика: {instance.person_name}\n"
        message += f"Номер телефона: {instance.phone_number}\n"
        message += f"Вид заказа: {instance.type_of_order}\n"

        if instance.as_soon_as_possible:
            message += "Как можно скорее\n"

        message += f"Дата и время забора заказа: {instance.order_date_time}\n"
        message += f"Филиал: {instance.filial}\n"

        if instance.address:
            message += f"Адрес: {instance.address}\n"
        if instance.apartment:
            message += f"Дом/квартира: {instance.apartment}\n"
        if instance.floor_and_code:
            message += f"Этаж и код от домофона: {instance.floor_and_code}\n"
        if instance.additional_to_order:
            message += f"Доп инфо к заказу: {instance.additional_to_order}\n"

        # Include the retrieved price in the message
        message += f"Цена: {price} сом\n"
        message += f"Транспорт: {instance.transport}"

        # Send the notification message with the price
        send_notification(message)
