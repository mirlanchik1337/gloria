from rest_framework.pagination import PageNumberPagination, CursorPagination


class CustomProductPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomProductCursorPagination(CursorPagination):
    page_size = 3
    ordering = 'id'
