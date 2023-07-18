from rest_framework import serializers
from apps.product.models import (Postcard, Flowers, SweetGift, Balloon)
from main.serializers import CategorySerializer


class PostcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postcard
        fields = ['photo_postcard', 'for_name', 'text', 'is_hit']


class FlowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowers
        fields = '__all__'
        # fields = ['image_flower', 'name_product', 'description', 'structure', 'price', 'is_hit']
        #


class SweetGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = SweetGift
        fields = '__all__'



class BalloonsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    class Meta:
        model = Balloon
        fields = '__all__'
