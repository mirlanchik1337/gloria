
from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination




class CustomProductPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 500


