from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from danube.contracts.views import ContractViewSet, WorkItemViewSet

app_name = "contracts"

list_dict = {"get": "list", "post": "create"}
detail_dict = {
    "get": "retrieve",
    "patch": "partial_update",
    "delete": "destroy",
}

urlpatterns = format_suffix_patterns(
    [
        path("contracts/", ContractViewSet.as_view(list_dict), name="contract-list"),
        path(
            "contracts/<int:pk>/",
            ContractViewSet.as_view({"get": "retrieve"}),
            name="contract-detail",
        ),
        path(
            "contracts/<int:pk>/send/",
            ContractViewSet.as_view({"post": "send"}),
            name="contract-send",
        ),
        path(
            "contracts/<int:pk>/costs/",
            ContractViewSet.as_view({"post": "costs"}),
            name="contract-costs",
        ),
        path(
            "contracts/<int:pk>/accept/",
            ContractViewSet.as_view({"post": "accept"}),
            name="contract-accept",
        ),
        path(
            "contracts/<int:pk>/decline/",
            ContractViewSet.as_view({"put": "decline"}),
            name="contract-decline",
        ),
        path(
            "contracts/<int:pk>/withdraw/",
            ContractViewSet.as_view({"put": "withdraw"}),
            name="contract-withdraw",
        ),
        path(
            "contracts/get_quote_or_contracts/",
            ContractViewSet.as_view({"get": "get_quote_or_contracts"}),
            name="contract-get_quote_or_contracts",
        ),
        path(
            "contracts/<int:pk>/complete/",
            ContractViewSet.as_view({"post": "complete"}),
            name="contract-complete",
        ),
        path(
            "work_items/",
            WorkItemViewSet.as_view({"post": "create"}),
            name="work_items-list",
        ),
        path(
            "work_items/<int:pk>/",
            WorkItemViewSet.as_view(detail_dict),
            name="work_items-detail",
        ),
    ]
)
