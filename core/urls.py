from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns_swagger
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.product.urls')),
    path('api/v1/', include('apps.cart.urls')),
    path('api/v1/', include("apps.users.urls"))
]+urlpatterns_swagger

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
