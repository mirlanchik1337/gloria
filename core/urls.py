from django.contrib import admin
from django.urls import path, include
from core.settings.yasg import urlpatterns_swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.product.urls')),
    path('api/v1/', include('apps.cart.urls')),
    path('api/v1/', include("apps.users.urls"))
]+urlpatterns_swagger


