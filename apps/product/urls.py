from django.urls import path
from .views import *
urlpatterns = [
    path('flower/', FlowerApiView.as_view()),
    path('flower/<int:pk>/', FlowersDetailView.as_view()),
    path('postcard/', PostcardApiView.as_view()),
    path('postcard/<int:pk>/', PostCardDetailView.as_view()),
    path('sweetgift/', SweetGiftApiView.as_view()),
    path('sweetgift/<int:pk>/', SweetGiftDetailView.as_view()),
    path('balloons/', BalloonApiView.as_view()),
    path('balloons/<int:pk>/', BalloonDetailView.as_view())
]
