from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics, status, request
from rest_framework.response import Response
from apps.cart.models import Order, CartItem, FavoriteProduct
from apps.cart.serializers import OrderSerializer, CartItemSerializer
from apps.product.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from telegram import Bot
import asyncio
from apps.cart.models import Order, Chat
from apps.product.services import send_notification
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.db import transaction
from django.utils import timezone


class OrderApiService(generics.ListCreateAPIView):
    serializer_class = OrderSerializer  # Use your Order serializer here

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        product = Product.objects.filter(user = user)

        # Check if the user has cart items
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and get the required fields from the request data
        person_name = request.data.get("person_name")
        phone_number = request.data.get("phone_number")
        type_of_order = request.data.get("type_of_order")
        postcard= product.postcard_set

        if not person_name or not phone_number or not type_of_order:
            return Response({"error": "person_name, phone_number, and type_of_order are required fields"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Ensure that type_of_order is a valid choice
        valid_type_choices = dict(Order.TYPE_ORDERING).keys()
        if type_of_order not in valid_type_choices:
            return Response({"error": f"Invalid type_of_order value. Choose from {valid_type_choices}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Calculate the total price
        price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
        price += postcard.price * len(postcard)

        try:
            with transaction.atomic():
                # Create the order
                order_data = {
                    "user": user,
                    "person_name": person_name,
                    "phone_number": phone_number,
                    "type_of_order": type_of_order,
                    "order_date_time": timezone.now(),
                    "price": price,
                    # Add other fields as needed
                }
                order_serializer = self.get_serializer(data=order_data)
                order_serializer.is_valid(raise_exception=True)
                order_serializer.save()

                # Associate cart items with the order and save each cart item
                for cart_item in cart_items:
                    cart_item.order = order_serializer.instance
                    cart_item.save()

                # Clear the user's cart
                cart_items.delete()

                # Set the filial_id as you were doing before
                if order_serializer.instance.filial and order_serializer.instance.filial.name_address:
                    order_serializer.instance.filial_id = order_serializer.instance.filial.name_address
                else:
                    order_serializer.instance.filial_id = 1

                order_serializer.instance.save()

            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@receiver(post_save, sender=Order, dispatch_uid="send_order_notification")
def send_order_notification(sender, instance, created, **kwargs):
    if created:
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

        total_price = instance.cart_items.aggregate(Sum('price'))['price__sum']
        message += f"Цена: {total_price} сом\n"
        message += f"Транспорт: {instance.transport}"

        try:
            chat = Chat.objects.get(bot_owner=True)
            asyncio.run(send_notification(chat.chat_id, message))
        except Chat.DoesNotExist:
            pass


class OrderDetailServiceApiView(generics.RetrieveDestroyAPIView):
    def list_order_detail(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        total_price = orders.aggregate(Sum('cart_items__price'))['cart_items__price__sum']
        return Response({"total_price": total_price, "details": serializer.data}, status=status.HTTP_200_OK)


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
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        # Фильтруем объекты, чтобы убедиться, что они существуют в базе данных
        cart_items = [item for item in cart_items if CartItem.objects.filter(pk=item.id).exists()]
        # Сериализуем данные cart_items
        serializer = self.get_serializer(cart_items, many=True)
        # Возвращаем только данные cart_items без обертки
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        cart_items.delete()
        return Response({"message": "Все объекты из корзины были успешно удалены."})

    def create(self, request, *args, **kwargs):
        data = request.data
        quantity = int(data.get('quantity', 1))
        # Проверяем, существует ли объект с указанным id в корзине пользователя
        product = data.get('product')
        existing_item = CartItem.objects.filter(user=request.user, product=product).first()

        if existing_item:
            existing_item.quantity += quantity  # Прибавляем к существующему количеству значение quantity
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data)
        else:
            data['quantity'] = quantity + 1   # Устанавливаем значение quantity в переданное значение или 1
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

