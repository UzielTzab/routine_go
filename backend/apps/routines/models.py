import uuid
from django.db import models
from django.conf import settings

class Category(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="Código único como hygiene, exercise, focus")
    name = models.CharField(max_length=100, help_text="Nombre visible")
    color_code = models.CharField(max_length=50, help_text="Variable CSS o Hex color")
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class RoutineTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='routines')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='routines')
    title = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    default_duration_minutes = models.PositiveIntegerField(default=30)
    priority = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'category', 'active']),
        ]

    def __str__(self):
        return self.title

class RoutineScheduleRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    routine = models.ForeignKey(RoutineTemplate, on_delete=models.CASCADE, related_name='schedule_rules')
    days_of_week = models.CharField(max_length=100, help_text="Días activos, ej: '0,1,2,3,4,5,6'")
    start_time = models.TimeField()
    reminder_minutes = models.PositiveIntegerField(default=0)
    timezone = models.CharField(max_length=50, default='UTC')
    auto_complete = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Rule for {self.routine.title} at {self.start_time}"
