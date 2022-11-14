from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import stripe
from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from djstripe.models import Price, Product
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response


from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from .serializers import ProductSerializer, PriceSerializer

# stripe.api_key = settings.STRIPE_SECRET_KEY

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY



class CreateCheckoutSessionView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        domain = "https://live-production-frontend.herokuapp.com/"
        # if settings.DEBUG:
        #     domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.id,
                    'adjustable_quantity': {
                        'enabled': True,
                        'minimum': 1,

                    },
                    'quantity': 1,
                }
            ],
            mode='subscription',
            success_url='https://live-production-frontend.herokuapp.com/success/',
            cancel_url='https://live-production-frontend.herokuapp.com/cancel/',
        )
        return JsonResponse({"url": checkout_session.url})





@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        payment_intent = session["payment_intent"]

        # TODO - send an email to the customer

    return Response(status=200)


# Handle the checkout.session.completed event


# Intent view 

class StripeIntentView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            price = Price.objects.get(id=self.kwargs["pk"])
            intent = stripe.PaymentIntent.create(
                amount=price.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "price_id": price.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
class ProductLandingPageView(ListAPIView):
    # template_name = "landing.html"

    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        product = Product.objects.all()
        return Response(ProductSerializer(product, many=True).data)

# custom payment view

class CustomPaymentView(ListAPIView):
    # template_name = "custom_payment.html"
    serializer_class = PriceSerializer

    def get(self, request, *args, **kwargs):
        prices = Price.objects.all()
        return Response(PriceSerializer(prices, many=True).data)


class SuccessView(ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response(data='Successfully paid', status=200)


class CancelView(TemplateView):
    pass
    # template_name = "cancel.html"
