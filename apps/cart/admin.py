from django.contrib import admin
from apps.cart.models import CartItem, FavoriteProduct, Banners , Cart

admin.site.register(CartItem)
admin.site.register(FavoriteProduct)
admin.site.register(Banners)
admin.site.register(Cart)

