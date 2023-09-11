# urls.py
from django.urls import path
from .views import (FavoriteItemListView, FavoriteItemDetailView,
                    CartItemListView, CartItemDetailView,
                    BannersViewSet, OrderApiView,
                    OrderDetailApiView , TransportListView,
                    PricePostCardView , FilialView)

urlpatterns = [
    path('cart-items/', CartItemListView.as_view(), name='cart-item-list'),
    path('cart-items/<int:id>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('favorite/', FavoriteItemListView.as_view()),
    path('favorite/<int:id>/', FavoriteItemDetailView.as_view()),
    path('banners/', BannersViewSet.as_view()),
    path('orders/', OrderApiView.as_view()),
    path('orders/<int:id>/', OrderDetailApiView.as_view()),
    path('transport/', TransportListView.as_view()),
    path('pricepostcard/', PricePostCardView.as_view()),
    path('filial/', FilialView.as_view()),

]
