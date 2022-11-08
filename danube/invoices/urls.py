from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from danube.invoices.views import InvoiceViewSet

app_name = "invoices"

list_dict = {"get": "list", "post": "create"}

urlpatterns = format_suffix_patterns(
    [
        path("invoices/", InvoiceViewSet.as_view(list_dict), name="invoice-list"),
        path(
            "invoices/<int:pk>/",
            InvoiceViewSet.as_view({"get": "retrieve"}),
            name="invoice-detail",
        ),
        path(
            "invoices/<int:pk>/paid/",
            InvoiceViewSet.as_view({"post": "paid"}),
            name="invoice-paid",
        ),
        path(
            "invoices/<int:pk>/paid_business/",
            InvoiceViewSet.as_view({"post": "paid_business"}),
            name="invoice-paid-business",
        ),
    ]
)
