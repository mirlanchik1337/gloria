from django.urls import path
from . import views

urlpatterns = [
    path("init_payment/", views.InitPaymentAPIView.as_view(), name="init_payment"),
    path("result_url/", views.ResultURLAPIView.as_view(), name="result_url"),
    # path("get_status/", views.GetStatusAPIView.as_view(), name="get_status"),
]
