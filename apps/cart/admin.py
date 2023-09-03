from django.contrib import admin
from apps.cart.models import CartItem, FavoriteProduct, Banners, Order, TypeOfOrder, Filial


class OrderAdmin(admin.ModelAdmin):
    list_display = ('person_name', 'phone_number')


admin.site.register(CartItem)
admin.site.register(FavoriteProduct)
admin.site.register(Banners)
admin.site.register(Order, OrderAdmin)
admin.site.register(TypeOfOrder)
admin.site.register(Filial)