from django.contrib import admin
from apps.product.models import (Product, Category, Subcategory)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'description', 'is_hit', 'is_sale', 'categories')
    list_filter = ('price', 'categories')
    search_fields = ('title', 'description')

    class Meta:
        ordering = ('title', 'price')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Subcategory)
