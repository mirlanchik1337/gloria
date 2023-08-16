from apps.product.models import (Product, Category,
                                 Subcategory, QuationsAnswers,
                                 Review, Stories, SecondSubcategory,
                                 PostCard, PostCardPrice,
                                 TitleOnBall, FontSize,
                                 ImageModel)

from django.contrib import admin


class ProductImageInline(admin.TabularInline):
    model = ImageModel
    min_num = 1
    max_num = 4
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'is_hit', 'categories')
    list_filter = ('price', 'categories')
    search_fields = ('name', 'description')
    prepopulated_fields = {'product_slug': ('name',)}
    inlines = (ProductImageInline,)

    class Meta:
        ordering = ('name', 'price')
        list_display = ("name", "price", "description", "is_hit", "categories")
        list_filter = ("price", "categories")
        search_fields = ("name", "description")

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


class SecondSubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "second_subcategory_slug")
    list_display_links = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {'second_subcategory_slug': ('name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Review)
admin.site.register(QuationsAnswers)
admin.site.register(Stories)
admin.site.register(SecondSubcategory, SecondSubcategoryAdmin)
admin.site.register(PostCard)
admin.site.register(ImageModel)
admin.site.register(PostCardPrice)
admin.site.register(TitleOnBall)
admin.site.register(FontSize)
