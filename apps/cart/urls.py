# urls.py
from django.urls import path
from .views import CartItemCreateView, CartItemDetailView, FavoriteCreateView, CartItemListView

urlpatterns = [
    path("cart/", CartItemCreateView.as_view(), name="cart-create"),
    path("carts/", CartItemListView.as_view(), name="cart-list"),
    path("cart/<int:pk>/", CartItemDetailView.as_view(), name="cart-detail"),
    path('favorite/', FavoriteCreateView.as_view(), name='add-to-favorites')
]
