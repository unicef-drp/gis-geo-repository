from django.urls import re_path
from dashboard.views.dashboard import DashboardView


urlpatterns = [
    re_path(r'', DashboardView.as_view(), name='dashboard-view')
]
