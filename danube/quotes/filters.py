import django_filters
from django_filters import rest_framework as filters

from danube.quotes.models import RFQBusinessRequest


class RFQBusinessFilterSet(filters.FilterSet):
    status: django_filters.CharFilter = filters.CharFilter(method="filter_by_status",)

    @staticmethod
    def filter_by_status(queryset, name, value):
        del name
        statuses_mapping = {v: k for k, v in RFQBusinessRequest.STATUS_CHOICES}
        mapped_value = statuses_mapping.get(value)
        if mapped_value:
            queryset.filter(status=mapped_value).distinct()
        else:
            return queryset

    class Meta:
        model = RFQBusinessRequest
        fields = {
            "business_profile": ("exact",),
        }
