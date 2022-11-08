from django.db.models import Sum, Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from danube.contracts.models import Contract
from danube.contracts.serializers import ContractSerializer, TopStatsContractsSerializer, ChartsContractsSerializer
from danube.invoices.models import Invoice
from danube.landing.models import Testimonial, FAQ
from danube.landing.serializers import TestimonialSerializer, FAQSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class TopStatsViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    @action(detail=False, methods=["get"])
    def get_contracts_stats(self, request):
        self.serializer_class = TopStatsContractsSerializer
        model = self.request.query_params.get('model')
        status = self.request.query_params.get('status')
        data = None
        if model == 'contract':
            if status == Contract.IN_PROGRESS:
                data = Contract.objects.filter(status__in=[Contract.IN_PROGRESS]).aggregate(count=Count('pk'),
                                                                                            amount=Sum('total'))
            else:
                data = Contract.objects.filter(status__in=[Contract.DONE]).aggregate(count=Count('pk'),
                                                                                     amount=Sum('total'))
        elif model == 'invoice':
            if status == Invoice.OPEN:
                data = Invoice.objects.filter(status__in=[Invoice.OPEN]).aggregate(count=Count('pk'),
                                                                                   amount=Sum('contract__total'),
                                                                                   c_status=Invoice.OPEN)
            else:
                data = Invoice.objects.filter(status__in=[Invoice.PAID]).aggregate(count=Count('pk'),
                                                                                   amount=Sum('contract__total'))
        data['status'] = status

        serialized = self.serializer_class(data)
        return Response(serialized.data)

class ChartsViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    @action(detail=False, methods=["get"])
    def get_charts_data(self, request):
        self.serializer_class = ChartsContractsSerializer
        model = self.request.query_params.get('model')
        status = self.request.query_params.get('status')
        year = self.request.query_params.get('year')
        data = None
        if model == 'contract':
            if status == Contract.IN_PROGRESS:
                data = Contract.objects.filter(status__in=[Contract.IN_PROGRESS], created_at__year=year).values('created_at__year', 'created_at__month').annotate(count=Count('pk'))
            else:
                data = Contract.objects.filter(status__in=[Contract.DONE], created_at__year=year).values('created_at__year', 'created_at__month').annotate(count=Count('pk'))
        elif model == 'invoice':
            if status == Invoice.OPEN:
                data = Invoice.objects.filter(status__in=[Invoice.OPEN], created_at__year=year).values('created_at__year', 'created_at__month').annotate(count=Count('pk'))
            else:
                data = Invoice.objects.filter(status__in=[Invoice.PAID], created_at__year=year).values('created_at__year', 'created_at__month').annotate(count=Count('pk'))
        data['status'] = status
        serialized = self.serializer_class(data)
        return Response(serialized.data)


