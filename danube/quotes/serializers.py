from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from danube.profiles.serializers import (
    PropertySerializer,
    PropertyShortSerializer,
    BusinessDetailsSerializer,
)
from danube.quotes.models import RFQ, RFQItem, RFQBusinessRequest, EOI


class RFQSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields["status"] = serializers.CharField(
            source="get_status_display", read_only=True
        )
        self.fields["rfq_items"] = RFQItemSerializer(many=True)
        self.fields["property"] = PropertySerializer()
        return super().to_representation(instance)

    class Meta:
        model = RFQ
        fields = [
            "id",
            "title",
            "status",
            # "profile",
            "property",
            # "send_to_market_place",
            # "business",
            "created_at",
            "rfq_items",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "rfq_items",
            "status",
        ]


class RFQItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = [
            "id",
            "rfq",
            "area_of_work",
            "brief_description",
            "detailed_description",
            "comments",
        ]


class RFQShortSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields["property"] = PropertyShortSerializer()
        self.fields["rfq_items"] = RFQItemSerializer(many=True)
        return super().to_representation(instance)

    class Meta:
        model = RFQ
        fields = ["id", "title", "rfq_items", "created_at"]


class RFQBusinessRequestSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField(method_name="get_owner_name")

    def get_owner_name(self, obj):
        return obj.rfq.property.user.first_name

    def to_representation(self, instance):
        self.fields["status"] = serializers.CharField(
            source="get_status_display", read_only=True
        )
        self.fields["rfq"] = RFQSerializer()
        return super().to_representation(instance)

    def create(self, validated_data):
        if validated_data["rfq"].status not in (RFQ.SAVED, RFQ.OPEN, RFQ.PRIVATE):
            raise ValidationError(
                f"RFQ with 'id={validated_data['rfq'].id}' doesn't have status SAVED/OPEN/PRIVATE."
            )
        return super().create(validated_data)

    class Meta:
        model = RFQBusinessRequest
        fields = [
            "id",
            "rfq",
            "business_profile",
            'owner_name'
        ]


class RFQBusinessCustomerSerializer(RFQBusinessRequestSerializer):
    def to_representation(self, instance):
        self.fields["rfq"] = RFQSerializer()
        return super().to_representation(instance)

    class Meta:
        model = RFQBusinessRequest
        fields = [
            "id",
            "status",
            "rfq",
            "business_profile",
        ]


class RFQBusinessEmployeeSerializer(RFQBusinessRequestSerializer):
    owner_name = serializers.SerializerMethodField(method_name="get_owner_name")

    def get_owner_name(self, obj):
        return obj.rfq.property.user.first_name

    def to_representation(self, instance):
        self.fields["rfq"] = RFQShortSerializer()
        return super().to_representation(instance)

    class Meta:
        model = RFQBusinessRequest
        fields = [
            "id",
            "status",
            "owner_name",
            "rfq",
            "business_profile",
        ]


class EOISerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields["status"] = serializers.CharField(
            source="get_status_display", read_only=True
        )
        return super().to_representation(instance)

    def create(self, validated_data):
        rfq = validated_data["rfq"]
        business = validated_data["business"]
        if rfq.status not in (RFQ.OPEN, RFQ.PRIVATE):
            raise ValidationError(
                f"RFQ with 'id={validated_data['rfq'].id}' doesn't have status OPEN/PRIVATE."
            )
        elif (
                rfq.status == RFQ.PRIVATE
                and not rfq.business_request.filter(business_profile_id=business.id).count()
        ):
            raise ValidationError(
                f"Business with ID {business.id} doesn't have access to the RFQ."
            )

        return super().create(validated_data)

    class Meta:
        model = EOI
        fields = [
            "id",
            "status",
            "rfq",
            "comment",
            "start_price",
            "created_at",
            "business",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]


class EOICustomerSerializer(EOISerializer):
    business_user_name = serializers.SerializerMethodField(
        method_name="get_business_user_name"
    )

    def get_business_user_name(self, obj):
        return obj.business.user.first_name

    def to_representation(self, instance):
        self.fields["rfq"] = RFQSerializer()
        self.fields["business"] = BusinessDetailsSerializer()
        return super().to_representation(instance)

    class Meta:
        model = EOI
        fields = [
            "id",
            "status",
            "rfq",
            "comment",
            "start_price",
            "created_at",
            "business",
            "business_user_name",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "business",
            "business_user_name",
        ]


class EOIBusinessSerializer(EOISerializer):
    customer_name = serializers.SerializerMethodField(method_name="get_customer_name")

    def get_customer_name(self, obj):
        return obj.rfq.property.user.first_name

    def to_representation(self, instance):
        self.fields["rfq"] = RFQShortSerializer()
        self.fields["business"] = BusinessDetailsSerializer()
        return super().to_representation(instance)

    class Meta:
        model = EOI
        fields = [
            "id",
            "status",
            "rfq",
            "comment",
            "start_price",
            "created_at",
            "business",
            "customer_name",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "customer_name",
        ]


class OpenOrPrivateSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=10)
