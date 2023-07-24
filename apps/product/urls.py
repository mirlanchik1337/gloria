from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.product.views import (ProductViewSet, CategoryViewSet, SubcategoryViewSet, ReviewViewSet)

router = DefaultRouter()
(router.register(r'products', ProductViewSet, basename='product'),
 router.register(r'categories', CategoryViewSet, basename='category'),
 router.register(r'subcategories', SubcategoryViewSet, basename='subcategory'),
 router.register(r'reviews', ReviewViewSet, basename='review'))
urlpatterns = router.urls
