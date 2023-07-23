from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.product.views import (ProductViewSet, CategoryViewSet, SubcategoryViewSet)

router = DefaultRouter()
(router.register(r'products', ProductViewSet, basename='product'),
 router.register(r'categories', CategoryViewSet, basename='category'),
 router.register(r'subcategories', SubcategoryViewSet, basename='subcategory'))
urlpatterns = router.urls
