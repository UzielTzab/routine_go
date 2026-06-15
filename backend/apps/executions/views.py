from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import RoutineExecution
from .serializers import RoutineExecutionDetailSerializer
from .services.state_machine import ExecutionStateMachineService

class RoutineExecutionViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin, viewsets.mixins.UpdateModelMixin):
    serializer_class = RoutineExecutionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return RoutineExecution.objects.filter(user=self.request.user)

    def _execute_transition(self, method, request, pk=None, **kwargs):
        execution = self.get_object()
        try:
            execution = method(execution, **kwargs)
            serializer = self.get_serializer(execution)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start(self, request, id=None):
        return self._execute_transition(ExecutionStateMachineService.start, request)

    @action(detail=True, methods=['post'])
    def pause(self, request, id=None):
        return self._execute_transition(ExecutionStateMachineService.pause, request)

    @action(detail=True, methods=['post'])
    def resume(self, request, id=None):
        return self._execute_transition(ExecutionStateMachineService.resume, request)

    @action(detail=True, methods=['post'])
    def complete(self, request, id=None):
        return self._execute_transition(ExecutionStateMachineService.complete, request)

    @action(detail=True, methods=['post'])
    def omit(self, request, id=None):
        return self._execute_transition(ExecutionStateMachineService.omit, request)

    @action(detail=True, methods=['post'])
    def snooze(self, request, id=None):
        minutes = int(request.data.get('minutes', 15))
        return self._execute_transition(ExecutionStateMachineService.snooze, request, minutes=minutes)
