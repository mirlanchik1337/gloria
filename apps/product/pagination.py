from rest_framework.pagination import PageNumberPagination


class CustomProductPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomСategoryPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 80
