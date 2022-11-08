from rest_framework import serializers

from danube.profiles.models import BusinessDetails, Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class PropertyShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["id", "postcode"]


class BusinessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetails
        fields = [
            "id",
            "user",
            "business_name",
            "website",
            "vat",
            "main_trade",
            "description",
            "company_number",
            "created_at",
            "address_1",
            "address_2",
            "town",
            "city",
            "county",
            "postcode",
        ]
