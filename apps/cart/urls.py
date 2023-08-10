# urls.py
from django.urls import path
from .views import FavoriteCreateSet, CartItemListSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
(
    router.register(r"favorite", FavoriteCreateSet, basename="favorite"),
    router.register(r"cart",CartItemListSet, basename="cart"),
)

urlpatterns = router.urls
