from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.product.views import (
    ProductViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    ReviewViewSet,
    QuationsAnswersViewSet,
    StoriesViewSet,
    WhatsAppLinkViewSet,
    SecondSubcategoryViewSet,
    PostCardViewSet, TitleOnBallViewSet
)

router = DefaultRouter()
(
    router.register(r"products", ProductViewSet, basename="product"),
    router.register(r"categories", CategoryViewSet, basename="category"),
    router.register(r"subcategories", SubcategoryViewSet, basename="subcategory"),
    router.register(r'reviews', ReviewViewSet, basename='review'),
    router.register(r"quationsanswers", QuationsAnswersViewSet, basename="quationsanswers"),
    router.register(r'stories', StoriesViewSet, basename='stories'),
    router.register(r'whatsapp', WhatsAppLinkViewSet, basename='whatsapp_link'),
    router.register(r'second-subcategories', SecondSubcategoryViewSet, basename='second_subcategory'),
    router.register(r'postcards', PostCardViewSet, basename='post_card'),
    router.register(r'titleonballs', TitleOnBallViewSet, basename='title_on_ball')
)

urlpatterns = router.urls
