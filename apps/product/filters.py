from django.db.models import Q
from django_filters import rest_framework as filter
from apps.product.models import Product, Category, Subcategory
from rest_framework import filters


class ProductFilters(filter.FilterSet):
    categories = filter.ModelChoiceFilter(queryset=Category.objects.all())
    subcategories = filter.ModelChoiceFilter(queryset=Subcategory.objects.all())
    price = filter.RangeFilter(field_name='price')
    quantity = filter.RangeFilter(field_name='quantity')


class CaseInsensitiveSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', None)
        if search_param:
            search_fields = getattr(view, 'search_fields', [])
            if search_fields:
                q_objects = Q()
                for field in search_fields:
                    q_objects |= Q(**{f'{field}__icontains': search_param})
                queryset = queryset.filter(q_objects)
        return queryset
