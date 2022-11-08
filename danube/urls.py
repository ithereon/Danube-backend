from django.contrib import admin
from django.urls import path, include, re_path

from danube.chat.routing import websocket_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="BillnTrade API",
        default_version="v1",
        description="BillnTrade description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

swagger_urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

urlpatterns = (
    [
        path("", include("danube.profiles.url")),
        path("", include("danube.quotes.urls")),
        path("accounts/", include("danube.accounts.url")),
        path("admin/", admin.site.urls),
        path("api-auth/", include("rest_framework.urls")),
        path("blogs/", include("blogs.urls")),
        path("", include("danube.landing.urls")),
        path("", include("danube.contracts.urls")),
        path("", include("danube.chat.urls")),
        path("", include("danube.invoices.urls")),
        path("payments/", include("danube.payments.urls")),
    ]
    + swagger_urlpatterns
    + websocket_urlpatterns
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
