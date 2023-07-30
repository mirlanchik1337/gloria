from rest_framework.routers import DefaultRouter

from apps.product.views import (
    ProductViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    ReviewViewSet,
    QuationsAnswersViewSet,
    StoriesViewSet
)

router = DefaultRouter()
(
    router.register(r"products", ProductViewSet, basename="product"),
    router.register(r"categories", CategoryViewSet, basename="category"),
    router.register(r"subcategories", SubcategoryViewSet, basename="subcategory"),
    router.register(r'reviews', ReviewViewSet, basename='review'),
    router.register(r"quationsanswers", QuationsAnswersViewSet, basename="quationsanswers"),
    router.register(r'stories', StoriesViewSet, basename='stories')
)

urlpatterns = router.urls
