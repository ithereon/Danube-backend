from decimal import Decimal

from rest_framework import serializers
from rest_framework.serializers import Serializer

from danube.contracts.models import WorkItem, Contract
from danube.profiles.serializers import (
    PropertyShortSerializer,
    BusinessDetailsSerializer,
    PropertySerializer,
)


class WorkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkItem
        fields = (
            "id",
            "title",
            "price",
            "contract",
            "description",
            "created_at",
        )
        
        read_only_fields = (
            "id",
            "created_at",
        )


class ContractSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField(method_name="get_owner_name")
    business_name = serializers.SerializerMethodField(method_name="get_business_name")

    def get_owner_name(self, obj):
        return obj.property_obj.user.first_name

    def get_business_name(self, obj):
        return obj.business.user.first_name

    def to_representation(self, instance):
        self.fields["status"] = serializers.CharField(source="get_status_display")
        self.fields["work_items"] = WorkItemSerializer(many=True, read_only=True)
        self.fields["property_obj"] = PropertySerializer()
        self.fields["business"] = BusinessDetailsSerializer()
        self.fields["total_cost"] = serializers.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0))
        self.fields["discount_amount"] = serializers.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0))
        self.fields["subtotal_after_discount"] = serializers.DecimalField(max_digits=8, decimal_places=2,
                                                                          default=Decimal(0))
        self.fields["vat_amount"] = serializers.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0))
        self.fields["total"] = serializers.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0))
        self.fields["total_after_first_payment"] = serializers.DecimalField(max_digits=8, decimal_places=2,
                                                                            default=Decimal(0))
        self.fields["first_payment_amount"] = serializers.DecimalField(max_digits=8, decimal_places=2,
                                                                       default=Decimal(0))

        return super().to_representation(instance)

    class Meta:
        model = Contract
        fields = (
            "id",
            "owner_name",
            "business_name",
            "title",
            "status",
            "business_completed",
            "work_items",
            "property_obj",
            "business",
            "description",
            "eoi",
            "total_cost",
            "discount_amount",
            "subtotal_after_discount",
            "vat_amount",
            "total",
            "first_payment_amount",
            "total_after_first_payment",
            "discount_type",
            "discount",
            "vat",
            "created_at",
        )
        read_only_fields = (
            "id",
            "owner_name",
            "business_name",
            "created_at",
            "status",
            "business_completed",
            "total_cost",
            "discount_amount",
            "subtotal_after_discount",
            "vat_amount",
            "total",
            "total_after_first_payment",
            "work_items",
        )


class QuoteOrContractSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=10)


class TopStatsContractsSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=20)
    count = serializers.IntegerField(allow_null=True)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0'))
    status = serializers.CharField(max_length=20)


class ChartsContractsSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=20)
    status = serializers.CharField(max_length=20)
    year = serializers.IntegerField(default=2022)
    count = serializers.IntegerField(allow_null=True)
    created_at__year = serializers.SerializerMethodField(read_only=True)
    created_at__month = serializers.SerializerMethodField(read_only=True)

    def get_created_at__year(self, instance):
        return [item for item in instance.all()]

    def get_created_at__month(self, instance):
        return [item for item in instance.all()]
