from rest_framework import serializers
from apps.executions.models import RoutineExecution
from apps.routines.serializers import RoutineTemplateSerializer

class RoutineExecutionSerializer(serializers.ModelSerializer):
    routine = RoutineTemplateSerializer(read_only=True)
    
    class Meta:
        model = RoutineExecution
        fields = [
            'id', 'routine', 'scheduled_start', 'scheduled_end',
            'actual_start', 'actual_end', 'duration_minutes',
            'status', 'notes', 'created_at', 'updated_at'
        ]
