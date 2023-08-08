# urls.py
from django.urls import path
from .views import CartItemDetailView, FavoriteCreateView, CartItemListView

urlpatterns = [
    path("cart/", CartItemListView.as_view(), name="cart-list"),
    path("cart/<int:pk>/", CartItemDetailView.as_view(), name="cart-detail"),
    path('favorite/', FavoriteCreateView.as_view(), name='add-to-favorites')
]
