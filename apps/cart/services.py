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


def calculate_order_volume(cart_items):
    order_volume = 0

    for cart_item in cart_items:
        product_volume = cart_item.product.volume
        quantity = cart_item.quantity
        order_volume += product_volume * quantity

    return order_volume



class OrderApiService(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        # Получить данные из запроса и передать их сериализатору
        serializer = self.get_serializer(data=request.data)

        # Проверить валидность данных
        if serializer.is_valid():
            order = Order.objects.filter(user=request.user)
            if order.cart_items.count() == 0:
                return Response({"error": "Корзина пуста. Создание заказа невозможно."}, status=status.HTTP_400_BAD_REQUEST)

            # Сохранить объект Order
            serializer.save()

            # Вернуть успешный ответ
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Вернуть ошибку в случае невалидных данных
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        cart_items = [item for item in cart_items if CartItem.objects.filter(pk=item.id).exists()]
        serializer = self.get_serializer(cart_items, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        cart_items.delete()
        return Response({"message": "Все объекты из корзины были успешно удалены."})

    def create(self, request, *args, **kwargs):
        data = request.data
        quantity = int(data.get('quantity', 1))
        product = data.get('product')
        existing_item = CartItem.objects.filter(user=request.user, product=product).first()

        if existing_item:
            existing_item.quantity += quantity  # Прибавляем к существующему количеству значение quantity
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data)
        else:
            data['quantity'] = quantity
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)



async def send_notification(chat_id, message):
    bot = Bot(token="6470236178:AAEvFdGt-NrVR6gAEI_bdWLbjdLC81ZigEE")
    await bot.send_message(chat_id=chat_id, text=message)


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
        message += f"Цена: {instance.total_price} сом\n"
        message += f"Транспорт: {instance.transport}"

        try:
            chat = Chat.objects.get(bot_owner=True)
            asyncio.run(send_notification(chat.chat_id, message))
        except Chat.DoesNotExist:
            pass
