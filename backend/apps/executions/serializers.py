from rest_framework import serializers
from .models import RoutineExecution
from apps.routines.serializers import RoutineTemplateSerializer

class RoutineExecutionDetailSerializer(serializers.ModelSerializer):
    routine = RoutineTemplateSerializer(read_only=True)

    class Meta:
        model = RoutineExecution
        fields = [
            'id', 'routine', 'scheduled_start', 'scheduled_end',
            'actual_start', 'actual_end', 'last_resumed_at',
            'duration_minutes', 'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'actual_start', 'actual_end', 'last_resumed_at', 'duration_minutes']
