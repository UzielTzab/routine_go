from django.contrib import admin
from .models import RoutineExecution

@admin.register(RoutineExecution)
class RoutineExecutionAdmin(admin.ModelAdmin):
    list_display = ('routine', 'user', 'scheduled_start', 'status')
    list_filter = ('status', 'scheduled_start')
    search_fields = ('routine__title', 'user__username')
