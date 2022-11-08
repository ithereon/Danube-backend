from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from danube.accounts.models import User
from danube.quotes.models import RFQ, RFQItem, RFQBusinessRequest, EOI
from danube.quotes.permissions import RFQBusinessRequestPermissions, EOIPermissions
from danube.quotes.serializers import (
    RFQSerializer,
    RFQItemSerializer,
    RFQBusinessRequestSerializer,
    EOISerializer,
    RFQBusinessCustomerSerializer,
    RFQBusinessEmployeeSerializer,
    EOIBusinessSerializer,
    EOICustomerSerializer, OpenOrPrivateSerializer,
)


class RFQViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RFQSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    search_fields = ["title", "property__postcode"]
    queryset = RFQ.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(property__user=user)
        else:
            return self.queryset.none()

    @action(detail=True, methods=["post"])
    def send(self, request, pk=None):
        rfq = self.get_object()
        if rfq.status in (RFQ.SAVED, RFQ.PRIVATE):
            rfq.status = RFQ.OPEN
            rfq.save()
            return Response("RFQ was send.")
        else:
            raise ValidationError("RFQ must have status SAVED or PRIVATE")


class RFQItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RFQItemSerializer
    queryset = RFQItem.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(rfq__property__user=user)
        else:
            return self.queryset.none()


class RFQBusinessRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, RFQBusinessRequestPermissions]
    serializer_class = RFQBusinessRequestSerializer
    queryset = RFQBusinessRequest.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    search_fields = [
        "rfq__status",
        "rfq__title",
        "business_profile__postcode",
    ]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_customer:
            return RFQBusinessCustomerSerializer
        else:
            return RFQBusinessEmployeeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == User.CUSTOMER:
                return self.queryset.filter(rfq__property__user=user)
            elif user.user_type == User.BUSINESS:
                return self.queryset.filter(business_profile__user=user)
        else:
            return self.queryset.none()

    @action(detail=True, methods=["post"])
    def decline(self, request, pk=None):
        rfq_request = self.get_object()
        self.check_object_permissions(request, rfq_request)

        if rfq_request.status == RFQBusinessRequest.WAITING:
            rfq_request.status = RFQBusinessRequest.DECLINED
            rfq_request.save()
            return Response("RFQ request for business was declined.")
        else:
            raise ValidationError("RFQ request must have status WAITING")

    @action(detail=False, methods=["get"])
    def getopenorprivate(self, request):
        self.serializer_class = OpenOrPrivateSerializer()
        query_param = self.request.query_params.get('status')
        queryset = self.filter_queryset(self.get_queryset())
        if query_param == 'OPEN':
            business_rfq = queryset.filter(rfq__status=RFQ.OPEN)
        elif query_param == 'PRIVATE':
            business_rfq = queryset.filter(rfq__status=RFQ.PRIVATE)
        else:
            return Response("Something went wrong")
        page = self.paginate_queryset(RFQBusinessRequestSerializer(business_rfq, many=True).data)
        return self.get_paginated_response(page)


class EOIViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, EOIPermissions]
    serializer_class = EOISerializer
    queryset = EOI.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    search_fields = ["rfq__status", "rfq__title", "business__postcode"]

    def get_serializer_class(self):
        if self.request.user.is_employee:
            return EOIBusinessSerializer
        elif self.request.user.is_customer:
            return EOICustomerSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == User.CUSTOMER:
                return self.queryset.filter(rfq__property__user=user)
            elif user.user_type == User.BUSINESS:
                return self.queryset.filter(business__user=user)
        else:
            return self.queryset.none()

    @action(detail=True, methods=["post"])
    def decline(self, request, pk=None):
        eoi = self.get_object()
        self.check_object_permissions(request, eoi)

        if eoi.status == EOI.NEW:
            eoi.status = EOI.DECLINED
            eoi.save()
            return Response("EOI request was declined.")
        else:
            raise ValidationError("EOI must have status NEW")
