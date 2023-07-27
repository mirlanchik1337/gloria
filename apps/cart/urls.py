# urls.py
from django.urls import path
from .views import CartItemListCreateView, CartItemDetailView, FavoriteCreateView

urlpatterns = [
    path("cart/", CartItemListCreateView.as_view(), name="cart-list-create"),
    path("cart/<int:pk>/", CartItemDetailView.as_view(), name="cart-detail"),
    path('favorite/', FavoriteCreateView.as_view(), name='add-to-favorites')
]
