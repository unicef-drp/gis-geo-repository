from django.conf.urls import url, include
from georepo.api_views.reference_layer_list import (
    ReferenceLayerList
)


urlpatterns = [
    url(r'^api/reference-layer-list/$',
         ReferenceLayerList.as_view(),
         name='reference-layer-list')
]
