from django.conf import settings
from django.db.models import Sum, Q

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

from apps.product.models import PostCard, Product


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

        # Create a new order
        new_order = serializer.save()

        with transaction.atomic():
            for cart_item in cart_items:
                cart_item.order = new_order
                cart_item.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return a success response

    def delete(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items:
            return Response(status=status.HTTP_204_NO_CONTENT)

        for cart_item in cart_items:
            cart_item.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)  # Return a success response


class OrderDetailServiceApiView(generics.RetrieveDestroyAPIView):
    def list_order_detail(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=False)
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

    def delete(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        cart_items.delete()
        return Response({"message": "All objects in the cart have been successfully deleted."})

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id

        product = data.get('product')
        quantity = int(data.get('quantity', 1))

        existing_item = CartItem.objects.filter(user=request.user, product=product).first()

        if existing_item:
            # Обновляем существующий объект
            existing_item.quantity += quantity
            existing_item.save()
            serializer = self.get_serializer(existing_item)
        else:
            # Создаем новый объект
            serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define the send_notification function (replace this with your actual notification logic)
import requests

TELEGRAM_BOT_TOKEN = '6470236178:AAEvFdGt-NrVR6gAEI_bdWLbjdLC81ZigEE'
TELEGRAM_CHAT_ID = '5416111170'  # The chat ID where you want to send notifications


def send_notification(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }

    try:
        response = requests.post(url, params=params)
        if response.status_code != 200:
            print(f"Failed to send Telegram notification: {response.status_code} - {response.text}")
        else:
            print(f"Notification sent successfully: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram notification: {str(e)}")


@receiver(post_save, sender=Order, dispatch_uid="send_order_notification")
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        api_url = 'https://gloria.geeks.kg/api/v1/orders/'  # Use Django settings for the API URL

        try:
            response = requests.post(api_url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            price_data = response.json()
            price = price_data.get('price')
        except:
            price = response.json()

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
