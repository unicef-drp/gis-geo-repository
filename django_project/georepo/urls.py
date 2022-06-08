from django.conf.urls import url
from django.urls import path
from georepo.api_views.reference_layer_list import (
    ReferenceLayerList
)
from georepo.api_views.reference_layer import ReferenceLayer


urlpatterns = [
    path('api/reference-layer/<uuid:uuid>/<str:entity_type>/',
        ReferenceLayer.as_view(),
        name='reference-layer'),
    path('api/reference-layer/list/',
         ReferenceLayerList.as_view(),
         name='reference-layer-list'),
]
