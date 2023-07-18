from django.contrib import admin
from django.urls import path, include
from main.views import CategoryApiView ,CategoryDetailApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.product.urls')),
    path('category/', CategoryApiView.as_view()),
    path('category/<int:pk>', CategoryDetailApiView.as_view())
]
