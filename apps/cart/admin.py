from django.contrib import admin
from apps.cart.models import (CartItem, FavoriteProduct,
                              Banners, Order,
                               Filial, Chat)


class CartItemInline(admin.StackedInline):
    model = CartItem

class OrderAdmin(admin.ModelAdmin):
    inlines = (CartItemInline,)
    list_display = ('person_name', 'phone_number')


class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'bot_owner')
    search_fields = ('chat_id', 'username')
    list_filter = ('bot_owner',)
    verbose_name = "Админ телеграм"
    verbose_name_plural = "Админ телеграма"


admin.site.register(CartItem)
admin.site.register(FavoriteProduct)
admin.site.register(Banners)
admin.site.register(Order, OrderAdmin)
admin.site.register(Filial)
admin.site.register(Chat)
