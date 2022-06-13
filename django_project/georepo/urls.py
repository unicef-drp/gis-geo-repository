from django.urls import path
from django.views.generic import TemplateView

from georepo.api_views.reference_layer_list import (
    ReferenceLayerList
)
from georepo.api_views.reference_layer import ReferenceLayer


urlpatterns = [
    path('layer-test/', TemplateView.as_view(
        template_name='test_layer.html'
    )),
    path(
        'api/reference-layer/<uuid:uuid>/<str:entity_type>/',
        ReferenceLayer.as_view(),
        name='reference-layer'),
    path(
        'api/reference-layer/list/',
        ReferenceLayerList.as_view(),
        name='reference-layer-list'),
]
