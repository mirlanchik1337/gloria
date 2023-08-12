# urls.py
from django.urls import path
from .views import FavoriteCreateSet, CartItemListSet , BannersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
(
    router.register(r"favorite", FavoriteCreateSet, basename="favorite"),
    router.register(r"cart",CartItemListSet, basename="cart"),
    router.register(r"banners", BannersViewSet, basename='banner')
)

urlpatterns = router.urls
