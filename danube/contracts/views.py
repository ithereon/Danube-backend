from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from danube.constants import PERCENT, AMOUNT
from danube.contracts.models import Contract, WorkItem
from danube.contracts.permissions import ContractPermissions, WorkItemPermissions
from danube.contracts.serializers import ContractSerializer, WorkItemSerializer, QuoteOrContractSerializer
from danube.invoices.models import Invoice


class WorkItemViewSet(viewsets.ModelViewSet):
    serializer_class = WorkItemSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        WorkItemPermissions,
    )
    queryset = WorkItem.objects.all()


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        ContractPermissions,
    )
    queryset = Contract.objects.all()
    filter_backends = (
        SearchFilter,
    )
    search_fields = [
        "status",
        "title",
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

    @action(detail=True, methods=["post"])
    def costs(self, request, pk=None):
        contract = self.get_object()
        self.check_object_permissions(request, contract)
        if contract.status == Contract.DRAFT:
            if "discount_type" in request.data.keys() and "discount" in request.data.keys():
                disc_type = int(request.data["discount_type"])
                if disc_type == PERCENT or disc_type == AMOUNT:
                    contract.discount_type = disc_type
                    contract.save()
                disc_amount = request.data["discount"]
                if 0 <= disc_amount <= 100:
                    contract.discount = disc_amount
                elif contract.discount_type == AMOUNT and 0 <= disc_amount <= contract.total_cost:
                    contract.discount = disc_amount
            if "vat" in request.data.keys():
                vat = request.data["vat"]
                if 0 <= vat <= 100:
                    contract.vat = vat
            if "first_payment" in request.data.keys():
                first_pay = request.data["first_payment"]
                if 0 <= first_pay <= contract.total_cost:
                    contract.first_payment_amount = first_pay
            contract.save()
            serialized = ContractSerializer(contract)
            return Response(serialized.data)
        else:
            raise ValidationError("Contract must have status DRAFT")

    @action(detail=True, methods=["post"])
    def send(self, request, pk=None):
        contract = self.get_object()
        self.check_object_permissions(request, contract)

        if contract.status == Contract.DRAFT:
            contract.status = Contract.WAITING
            contract.save()
            return Response("Contract was sent to customer.")
        else:
            raise ValidationError("Contract must have status DRAFT")

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        contract = self.get_object()
        self.check_object_permissions(request, contract)
        if contract.status == Contract.WAITING:
            contract.status = Contract.IN_PROGRESS
            contract.save()
            return Response("Contract has started.")
        else:
            raise ValidationError("Contract must have status WAITING")

    @action(detail=True, methods=["put"])
    def decline(self, request, pk=None):
        if request.user.is_customer:
            contract = self.get_object()
            self.check_object_permissions(request, contract)
            if contract.status == Contract.WAITING:
                contract.status = Contract.REJECTED
                contract.save()
                return Response("Contract has been declined.")
            else:
                raise ValidationError("Contract must have status IN_PROGRESS")
        return Response("This user has no permission to decline contracts.")

    @action(detail=True, methods=["put"])
    def withdraw(self, request, pk=None):
        if request.user.is_employee:
            contract = self.get_object()
            self.check_object_permissions(request, contract)
            if contract.status == Contract.WAITING:
                contract.status = Contract.DRAFT
                contract.save()
                return Response("Contract has been withdrawn.")
            else:
                raise ValidationError("Contract must have status WAITING")
        else:
            return Response("This user has no permission to withdraw contracts.")

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        contract = self.get_object()
        self.check_object_permissions(request, contract)
        if request.user.is_employee:
            if contract.business_completed:
                raise ValidationError("Contract is already complete.")
            elif contract.status != Contract.IN_PROGRESS and contract.status != Contract.DONE:
                raise ValidationError("Contract must have 'in progress' status to make it complete.")
            else:
                contract.business_completed = True
                contract.save()
                return Response("Contract has been completed.")
        elif request.user.is_customer:
            if contract.status != Contract.IN_PROGRESS:
                raise ValidationError("Contract must have 'in progress' status to make it complete.")
            else:
                contract.status = Contract.DONE
                contract.save()
                return Response("Contract has been completed.")
        else:
            return Response("This user has no permission to complete contracts.")

    @action(detail=False, methods=["get"])
    def get_quote_or_contracts(self, request):
        self.serializer_class = QuoteOrContractSerializer()
        query_param = self.request.query_params.get('category')
        queryset = self.filter_queryset(self.get_queryset())
        if query_param == 'quote':
            contract = queryset.filter(status__in=[Contract.WAITING, Contract.DRAFT, Contract.REJECTED])
        elif query_param == 'contract':
            contract = queryset.filter(status__in=[Contract.IN_PROGRESS, Contract.DONE])
        else:
            return Response("Something went wrong")
        page = self.paginate_queryset(ContractSerializer(contract, many=True).data)
        return self.get_paginated_response(page)
