from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.product.views import (ProductViewSet, CategoryViewSet, SubcategoryViewSet,
                                ProductDetailApiView, CategoryDetailApiView, SubcategoryDetailApiView)

urlpatterns = [
    path('api/v1/products/<int:pk>', ProductDetailApiView.as_view()),
    path('api/v1/categories/<int:pk>', CategoryDetailApiView.as_view()),
    path('api/v1/subcategories/<int:pk>', SubcategoryDetailApiView.as_view()),
]
router = DefaultRouter()
(router.register(r'products', ProductViewSet, basename='product'),
 router.register(r'categories', CategoryViewSet, basename='category'),
 router.register(r'subcategories', SubcategoryViewSet, basename='subcategory'))
urlpatterns += router.urls
