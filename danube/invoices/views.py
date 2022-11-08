from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from danube.contracts.models import Contract
from danube.invoices.models import Invoice
from danube.invoices.permissions import InvoicePermissions
from danube.invoices.serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        InvoicePermissions,
    )
    queryset = Invoice.objects.all()
    filter_backends = (
        SearchFilter,
    )
    search_fields = [
        "status",
        "contract__title",
        "property_obj__postcode",
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_customer:
                return self.queryset.filter(property_obj__user=user)
            elif user.is_employee:
                return self.queryset.filter(business__user=user)
        else:
            return self.queryset.none()

    def create_invoice(self, contract):
        invoice = self.create(contract=contract)
        return invoice

    @action(detail=True, methods=["post"])
    def paid(self, request, pk=None):
        invoice = self.get_object()
        self.check_object_permissions(request, invoice)
        if invoice.status == Invoice.OPEN:
            if invoice.contract.first_payment_paid or invoice.contract.first_payment_amount <= 0:
                invoice.status = Invoice.PAID
                invoice.save()
                serialized = InvoiceSerializer(invoice)
                return Response(serialized.data)
            else:
                invoice.status = Invoice.PENDING
                invoice.save()
                contract = Contract.objects.filter(id=invoice.contract.id).get()
                contract.first_payment_paid = True
                contract.save()
                serialized = InvoiceSerializer(invoice)
                return Response(serialized.data)
        else:
            raise ValidationError("Invoice is already paid.")

    @action(detail=True, methods=["post"])
    def paid_business(self, request, pk=None):
        invoice = self.get_object()
        self.check_object_permissions(request, invoice)
        if invoice.status_business == Invoice.OPEN:
            if invoice.contract.first_payment_paid_business or invoice.contract.first_payment_amount <= 0:
                invoice.status_business = Invoice.PAID
                invoice.save()
                serialized = InvoiceSerializer(invoice)
                return Response(serialized.data)
            else:
                invoice.status_business = Invoice.PENDING
                invoice.save()
                contract = Contract.objects.filter(id=invoice.contract.id).get()
                contract.first_payment_paid_business = True
                contract.save()
                serialized = InvoiceSerializer(invoice)
                return Response(serialized.data)
        else:
            raise ValidationError("Invoice is already paid.")
