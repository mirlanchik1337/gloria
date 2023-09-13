from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from telegram import Bot
import asyncio
from apps.cart.models import Order, CartItem, Product, Chat


async def send_notification(chat_id, message):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
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
        message += f"Цена: {instance.price} сом\n"
        message += f"Транспорт: {instance.transport}"

        # Отправляем уведомление владельцу бота
        try:
            chat = Chat.objects.get(bot_owner=True)
            asyncio.run(send_notification(chat.chat_id, message))
        except Chat.DoesNotExist:
            pass
