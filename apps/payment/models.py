from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .settings import PaymentStatus
from apps.product.models import Order
User = get_user_model()


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
        verbose_name=_("пользователь"),
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Заказ/Корзина"),
        related_name="transaction",
    )
    payment_id = models.CharField(
        max_length=125,
        null=True,
        blank=True,
        verbose_name=_("id платежа в системе FreedomPay"),
    )
    pg_salt = models.CharField(
        max_length=125,
        null=True,
        blank=True,
        verbose_name=_("salt(рандомное слово) платежа в системе FreedomPay"),
    )
    pg_description = models.TextField(null=True, blank=True, verbose_name=_("Описание"))
    currency = models.CharField(
        max_length=20, null=True, blank=True, verbose_name=_("Валюта")
    )
    payment_method = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("метод оплаты")
    )
    payment_date = models.DateTimeField(
        auto_now=True, verbose_name=_("Дата оплаты"), null=True
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=False,
        null=True,
        verbose_name=_("Сумма"),
    )
    status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("статус"),
    )
    pg_card_pan = models.CharField(
        max_length=250, null=True, blank=True, verbose_name=_("Номер карты")
    )
    pg_sig = models.CharField(
        max_length=250, null=True, blank=True, verbose_name=_("Подпись")
    )
    pg_result = models.CharField(
        max_length=250, null=True, blank=True, verbose_name=_("рузультат оплаты")
    )
    pg_user_phone = models.CharField(
        max_length=250, null=True, blank=True, verbose_name=_("контактный номер тефона")
    )
    pg_user_contact_email = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name=_("контактный адрес Е-почты"),
    )
    pg_failure_description = models.TextField(
        null=True, blank=True, verbose_name=_("Описание неудачной оплаты")
    )

    def __str__(self):
        return f"пользователь: {self.user} сумма: {self.amount} дата: {self.payment_date} статус: {self.status}"

    class Meta:
        db_table = "transactions"
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
