from django.contrib import admin
from apps.cart.models import CartItem, FavoriteProduct, Banners

admin.site.register(CartItem)
admin.site.register(FavoriteProduct)
admin.site.register(Banners)
