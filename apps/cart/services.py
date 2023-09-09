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


class OrderApiService(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        # Вычисляем общую цену заказа
        total_price = sum(cart_item.price * cart_item.quantity for cart_item in cart_items)

        order = Order.objects.create(user=user, order_date_time=timezone.now(), total_price=total_price)

        # Связываем элементы корзины с заказом
        order.cart_items.set(cart_items)

        # Устанавливаем филиал
        if order.filial and order.filial.name_address:
            order.filial_id = order.filial.name_address
        else:
            order.filial_id = 1

        order.save()
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get_price(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        total_price = orders.aggregate(Sum('cart_items__price'))['cart_items__price__sum']
        return Response({"total_price": total_price}, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_quantity(self, request, product_id):
        cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
        if cart_item:
            product = Product.objects.get(id=product_id)
            quantity = product.quantity - cart_item.quantity
            product.quantity = quantity
            product.save()
            return Response({"quantity": quantity}, status=status.HTTP_200_OK)
        return Response({"message": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    def get_transport(self, request):
        return Response({"transport": self.kwargs.get('transport')}, status=status.HTTP_200_OK)


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

