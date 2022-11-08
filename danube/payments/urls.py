from django.urls import path
from django.contrib import admin
from . views import (
    CreateCheckoutSessionView,
    SuccessView,
    CancelView,
    ProductLandingPageView,
    stripe_webhook,
    StripeIntentView,
    CustomPaymentView,
)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', ProductLandingPageView.as_view(), name='landing'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('custom-payment/', CustomPaymentView.as_view(), name='custom-payment'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]