from django_filters import rest_framework as filters
from apps.product.models import Product, Category, Subcategory


class ProductFilters(filters.FilterSet):
    categories = filters.ModelChoiceFilter(queryset=Category.objects.all())
    subcategories = filters.ModelChoiceFilter(queryset=Subcategory.objects.all())
    price = filters.RangeFilter(field_name='price')
    quantity = filters.RangeFilter(field_name='quantity')

