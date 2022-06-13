# coding=utf-8
"""Main django urls."""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


schema_view = get_schema_view(
    openapi.Info(
        title="GeoRepo API",
        default_version='v0.1.0',
        description="GeoRepo API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

admin.autodiscover()

urlpatterns = [
    url(r'^$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'', include('georepo.urls')),
    url(r'', include('dashboard.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
