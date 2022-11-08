from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TITLES_CHOICE, Property, BusinessDetails
from .permissions import BusinessDetailsPermissions, UserProfilePermission
from .serializers import (
    PropertySerializer,
    BusinessDetailsSerializer,
)


class TitleView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs) -> Response:
        """
        Get the profile titles.
        """
        return Response(list(dict(TITLES_CHOICE).values()))


class PropertyViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        UserProfilePermission,
    ]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]
    search_fields = ["address_1", "address_2", "town", "city", "county", "postcode"]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Property.objects.filter(user=user)
        else:
            return Property.objects.none()


class BusinessDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        BusinessDetailsPermissions,
    ]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_fields = ["user"]
    search_fields = ["business_name", "website", "main_trade", "description"]
    serializer_class = BusinessDetailsSerializer
    queryset = BusinessDetails.objects.all()
