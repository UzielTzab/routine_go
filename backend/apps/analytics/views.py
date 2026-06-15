from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services.dashboard_service import DashboardService

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = DashboardService.get_dashboard_data(request.user)
        return Response(data)

from apps.analytics.services.reports import ReportsService

class ReportsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        report_data = ReportsService.get_full_report(request.user)
        return Response(report_data)
