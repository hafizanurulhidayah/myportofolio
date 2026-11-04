from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # Main application
    path("", include("main.urls")),

    # API
    path(
        "api/v1/",
        include(("main.api_urls", "api"), namespace="api")
    ),
    path("api-auth/", include("rest_framework.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)