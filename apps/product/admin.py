from apps.product.models import Product, Category, Subcategory, QuationsAnswers, Review, Stories
from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'is_hit', 'is_sale', 'categories')
    list_filter = ('price', 'categories')
    search_fields = ('title', 'description')
    prepopulated_fields = {'product_slug': ('name',)}

    class Meta:
        ordering = ('name', 'price')
        list_display = ("title", "price", "description", "is_hit", "is_sale", "categories")
        list_filter = ("price", "categories")
        search_fields = ("title", "description")

    class Meta:
        ordering = ("title", "price")

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = "Categories"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", 'category_slug')
    list_display_links = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {'category_slug': ('name',)}


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "subcategory_slug")
    list_display_links = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {'subcategory_slug': ('name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Review)
admin.site.register(QuationsAnswers)
admin.site.register(Stories)
