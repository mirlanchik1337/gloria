from apps.product.models import (Product, Category, Subcategory)
from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'description', 'is_hit', 'is_sale', 'categories')
    list_filter = ('price', 'categories')
    search_fields = ('title', 'description')

    class Meta:
        ordering = ('title', 'price')

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = 'Categories'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Subcategory)
