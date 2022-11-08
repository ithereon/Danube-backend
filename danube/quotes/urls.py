from rest_framework import routers
from django.urls import path, include

from danube.quotes.views import (
    RFQViewSet,
    RFQItemViewSet,
    RFQBusinessRequestViewSet,
    EOIViewSet,
)

app_name: str = "quotes"

router = routers.DefaultRouter()

router.register("rfq", RFQViewSet, basename="rfq")
router.register("rfq_items", RFQItemViewSet, basename="rfq_items")
router.register("rfq_business", RFQBusinessRequestViewSet, basename="rfq_business")
router.register("eoi", EOIViewSet, basename="eoi")

urlpatterns = [
    path("", include(router.urls)),
]
