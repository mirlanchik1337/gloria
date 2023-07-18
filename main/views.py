from django.shortcuts import render
from main.serializers import Category, CategorySerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView


class CategoryApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailApiView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
