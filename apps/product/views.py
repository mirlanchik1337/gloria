from rest_framework.response import Response
from apps.product.models import Postcard, Flowers, SweetGift, Balloon
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.product.serializers import FlowersSerializer, BalloonsSerializer, SweetGiftSerializer, PostcardSerializer


class FlowerApiView(ListAPIView):
    queryset = Flowers.objects.all()
    serializer_class = FlowersSerializer


class PostcardApiView(ListAPIView):
    queryset = Postcard.objects.all()
    serializer_class = PostcardSerializer


class BalloonApiView(ListAPIView):
    queryset = Balloon.objects.all()
    serializer_class = BalloonsSerializer


class SweetGiftApiView(ListAPIView):
    queryset = SweetGift.objects.all()
    serializer_class = SweetGiftSerializer


class FlowersDetailView(RetrieveAPIView):
    queryset = Flowers.objects.all()
    serializer_class = FlowersSerializer


class PostCardDetailView(RetrieveAPIView):
    queryset = Postcard.objects.all()
    serializer_class = PostcardSerializer


class BalloonDetailView(RetrieveAPIView):
    queryset = Balloon.objects.all()
    serializer_class = BalloonsSerializer


class SweetGiftDetailView(RetrieveAPIView):
    queryset = SweetGift.objects.all()
    serializer_class = SweetGiftSerializer
