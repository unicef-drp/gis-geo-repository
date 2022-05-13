from django.conf.urls import url
from dashboard.views.dashboard import DashboardView


urlpatterns = [
    url(r'', DashboardView.as_view(), name='dashboard-view')
]
