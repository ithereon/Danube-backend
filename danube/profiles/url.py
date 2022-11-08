from rest_framework import routers
from django.urls import path, include

from danube.profiles.views import (
    BusinessDetailsViewSet,
    PropertyViewSet,
    TitleView,
)

app_name: str = "profiles"

router = routers.DefaultRouter()

router.register("business_details", BusinessDetailsViewSet, basename="business_details")
router.register("properties", PropertyViewSet, basename="property")

urlpatterns = [
    path("titles/", TitleView.as_view(), name="title",),
    path("", include(router.urls)),
]
