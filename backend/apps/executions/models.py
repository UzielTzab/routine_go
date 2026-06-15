import uuid
from django.db import models
from django.conf import settings
from apps.routines.models import RoutineTemplate

class RoutineExecution(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('NOTIFIED', 'Notificada'),
        ('SNOOZED', 'Pospuesta'),
        ('IN_PROGRESS', 'En Progreso'),
        ('PAUSED', 'Pausada'),
        ('COMPLETED', 'Completada'),
        ('OMITTED', 'Omitida'),
        ('EXPIRED', 'Expirada'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='executions')
    routine = models.ForeignKey(RoutineTemplate, on_delete=models.CASCADE, related_name='executions')
    
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    last_resumed_at = models.DateTimeField(null=True, blank=True)
    
    duration_minutes = models.PositiveIntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)
    notification_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'scheduled_start']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'scheduled_start', 'status']),
        ]

    def __str__(self):
        return f"{self.routine.title} - {self.scheduled_start.date()} ({self.status})"
