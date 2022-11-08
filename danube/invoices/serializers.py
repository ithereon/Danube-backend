from rest_framework import serializers

from danube.contracts.serializers import ContractSerializer
from danube.invoices.models import Invoice
from danube.profiles.serializers import (
    BusinessDetailsSerializer,
    PropertySerializer,
)


class InvoiceSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField(method_name="get_owner_name")
    business_name = serializers.SerializerMethodField(method_name="get_business_name")

    def get_owner_name(self, obj):
        return obj.property_obj.user.first_name

    def get_business_name(self, obj):
        return obj.business.user.first_name

    def to_representation(self, instance):
        self.fields["status"] = serializers.CharField(source="get_status_display")
        self.fields["status_business"] = serializers.CharField(source="get_status_business_display")
        self.fields["property_obj"] = PropertySerializer()
        self.fields["business"] = BusinessDetailsSerializer()
        self.fields["contract"] = ContractSerializer()
        return super().to_representation(instance)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "owner_name",
            "business_name",
            "status",
            "status_business",
            "property_obj",
            "business",
            "contract",
            "eoi",
            "created_at",
        )
        read_only_fields = (
            "id",
            "owner_name",
            "business_name",
            "created_at",
            "status",
            "status_business",
        )
