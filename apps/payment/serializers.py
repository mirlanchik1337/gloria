from rest_framework import serializers

from .models import Transaction
from apps.product.settings import OrderStatus, PaymentTypeForOrder
from apps.users.serializers import UserSerializer
from products.serializers import OrderSerializer, CartItemSerializer


class InitPaymentSerialiizer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "user", "order")
        read_only_fields = ["user"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = UserSerializer(instance.user).data
        data["order"] = OrderSerializer(instance.order).data
        return data


class ResultURLSerializers(serializers.Serializer):
    pg_order_id = serializers.CharField(required=True)
    pg_payment_id = serializers.CharField(required=True)
    pg_payment_date = serializers.DateTimeField(required=False)
    pg_result = serializers.IntegerField(required=True)
    pg_salt = serializers.CharField(required=True)
    pg_sig = serializers.CharField(required=True)


class PaymentHistorySerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)
    payment_id = serializers.CharField(read_only=True)
    pg_salt = serializers.CharField(read_only=True)
    pg_description = serializers.CharField(read_only=True)
    currency = serializers.CharField(read_only=True)
    payment_method = serializers.CharField(read_only=True)
    payment_date = serializers.DateField(read_only=True)
    amount = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)


class BaskerInnerOrderSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.CharField(read_only=True)


class OrderHistorySerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    order_id = serializers.CharField(read_only=True)
    basket = BaskerInnerOrderSerializer(read_only=True)
    payment_type = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
