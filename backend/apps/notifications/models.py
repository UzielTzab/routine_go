import uuid
from django.db import models
from django.conf import settings
from apps.executions.models import RoutineExecution

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    execution = models.ForeignKey(RoutineExecution, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
