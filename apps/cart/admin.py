from django.contrib import admin
from apps.cart.models import CartItem, FavoriteProduct

admin.site.register(CartItem)
admin.site.register(FavoriteProduct)
