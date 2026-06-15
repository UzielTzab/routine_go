from django.urls import path
from apps.analytics.views import DashboardView, ReportsAPIView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='analytics-dashboard'),
    path('reports/', ReportsAPIView.as_view(), name='reports'),
]
