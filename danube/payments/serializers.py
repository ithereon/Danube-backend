from djstripe.models import Price, Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Price
        fields = '__all__'
