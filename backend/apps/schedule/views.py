from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .services.agenda_service import get_today_agenda
from .serializers import RoutineExecutionSerializer

class TodayScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Generar o recuperar la agenda de hoy
        executions = get_today_agenda(request.user)
        serializer = RoutineExecutionSerializer(executions, many=True)
        return Response(serializer.data)
