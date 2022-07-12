from django.urls import re_path
from dashboard.views.dashboard import DashboardView
from dashboard.views.uploader import UploaderView
from dashboard.api_views.layer_upload import (
    LayerUploadView,
    LayersProcessView,
    LayerRemoveView
)


urlpatterns = [
    re_path(
        r'upload/?$',
        UploaderView.as_view(),
        name='upload'
    ),
    re_path(
        r'api/layer-upload/?$',
        LayerUploadView.as_view(),
        name='layer-upload'
    ),
    re_path(
        r'api/layer-remove/?$',
        LayerRemoveView.as_view(),
        name='layer-remove'
    ),
    re_path(
        r'api/layers-process/?$',
        LayersProcessView.as_view(),
        name='layers-process'
    ),
    re_path(r'', DashboardView.as_view(), name='dashboard-view'),
]
