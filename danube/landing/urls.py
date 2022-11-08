from django.urls import path

from danube.landing.views import TestimonialViewSet, FAQViewSet, TopStatsViewSet, ChartsViewSet

app_name = "landing"

urlpatterns = [
    path(
        "testimonials/",
        TestimonialViewSet.as_view({"get": "list"}),
        name="testimonials-list",
    ),
    path("faq/", FAQViewSet.as_view({"get": "list"}), name="faq-list", ),
    path(
        "dashboard/get_contracts_stats/",
        TopStatsViewSet.as_view({"get": "get_contracts_stats"}),
        name="get_contracts_stats",
    ),
    path(
        "dashboard/get_charts_data/",
        ChartsViewSet.as_view({"get": "get_charts_data"}),
        name="get_charts_data",
    ),
]
