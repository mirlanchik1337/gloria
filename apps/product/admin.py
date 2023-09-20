from apps.product.models import (Product, Category,
                                 Subcategory, QuationsAnswers,
                                 Review, Stories, SecondSubcategory,
                                 PostCard, PostCardPrice,
                                 Balls, FontSize,
                                 ImageModel, Transport)

from django.contrib import admin


class BallsInline(admin.TabularInline):
    model = Balls
    min_num = 1
    max_num = 1
    extra = 0

    def __init__(self, *args, **kwargs):
        super(BallsInline, self).__init__(*args, **kwargs)
        self.extra = 1


class PostCardInline(admin.TabularInline):
    model = PostCard
    min_num = 1
    max_num = 10
    extra = 0

    def __init__(self, *args, **kwargs):
        super(PostCardInline, self).__init__(*args, **kwargs)
        self.extra = 1


class ProductImageInline(admin.TabularInline):
    model = ImageModel
    min_num = 1
    max_num = 10
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'is_hit', 'categories')
    list_filter = ('price', 'categories')
    search_fields = ('name', 'description')
    prepopulated_fields = {'product_slug': ('name',)}
    inlines = (ProductImageInline, PostCardInline, BallsInline)

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


class TransportAdmin(admin.ModelAdmin):
    list_display = ('model', 'price', 'min_volume', 'max_volume')


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
admin.site.register(Balls)
admin.site.register(FontSize)
admin.site.register(Transport, TransportAdmin)
