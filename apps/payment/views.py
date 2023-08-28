from rest_framework import generics, permissions, status, response
from rest_framework.reverse import reverse

from .services import PaymentService
from .serializers import InitPaymentSerialiizer, ResultURLSerializers
from .settings import success_url


class InitPaymentAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InitPaymentSerialiizer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = PaymentService.create_transaction(
            user=request.user,
            amount=serializer.validated_data.get("order").basket.total,
            order=serializer.validated_data.get("order"),
        )

        link = PaymentService.payment(
            pg_order_id=transaction.id,
            pg_amount=transaction.amount,
            pg_description=transaction.pg_description,
            pg_salt=transaction.user.email,
            pg_result_url=str(self.request.build_absolute_uri(reverse("result_url"))),
            pg_success_url=success_url,
            pg_success_url_method="GET",
        )
        return response.Response(
            data={"data": link["response"]},
            status=status.HTTP_200_OK
            if link["response"]["pg_status"] == "ok"
            else status.HTTP_400_BAD_REQUEST,
        )


class ResultURLAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ResultURLSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = PaymentService.result_url(
            pg_order_id=serializer.validated_data.get("pg_order_id"),
            pg_payment_id=serializer.validated_data.get("pg_payment_id"),
            pg_salt=serializer.validated_data.get("pg_salt"),
            pg_sig=serializer.validated_data.get("pg_sig"),
            pg_payment_date=serializer.validated_data.get("pg_payment_date"),
            pg_result=serializer.validated_data.get("pg_result"),
        )
        link_url = self.request.build_absolute_uri("/")
        text = message_card_payment_info(data.first().id, link_url)
        TelegramService.send_order(text)
        res = PaymentService.answer(pg_status=data.first().pg_result)
        return response.Response(data=res)
