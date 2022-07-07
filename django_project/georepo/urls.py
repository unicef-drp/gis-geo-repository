from django.urls import path, re_path, include
from django.views.generic import TemplateView

from georepo.api_views.reference_layer_list import (
    ReferenceLayerList
)
from georepo.api_views.reference_layer import (
    ReferenceLayerGeojson,
    ReferenceLayerEntityList,
    ReferenceLayerDetail
)
from georepo.api_views.protected_api import ProtectedApi


urlpatterns = [
    path('layer-test/', TemplateView.as_view(
        template_name='test_layer.html'
    )),
    re_path(r'^o/',
            include('oauth2_provider.urls',
                    namespace='oauth2_provider')),
    re_path(
        r'api/reference-layer/(?P<uuid>[\da-f-]+)/(?P<entity_type>\w+)/?$',
        ReferenceLayerGeojson.as_view(),
        name='reference-layer-geojson'),
    re_path(
        r'api/reference-layer/(?P<uuid>[\da-f-]+)/'
        r'(?P<entity_type>\w+)/list/?$',
        ReferenceLayerEntityList.as_view(),
        name='reference-layer-entity-list'),
    re_path(
        r'api/reference-layer/(?P<uuid>[\da-f-]+)/?$',
        ReferenceLayerDetail.as_view(),
        name='reference-layer-detail'),
    re_path(
        r'api/reference-layer/list/?$',
        ReferenceLayerList.as_view(),
        name='reference-layer-list'),
    re_path(
        r'api/protected/?$',
        ProtectedApi.as_view(),
        name='protected-api'
    )
]
