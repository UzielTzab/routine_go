from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from apps.executions.models import RoutineExecution

class ExecutionStateMachineService:
    """
    State machine for RoutineExecutions ensuring valid transitions and tracking time.
    """

    @classmethod
    def _validate_not_terminal(cls, execution):
        if execution.status in ['COMPLETED', 'OMITTED']:
            raise ValidationError(f"Cannot change status of a {execution.status} execution.")

    @classmethod
    @transaction.atomic
    def start(cls, execution: RoutineExecution) -> RoutineExecution:
        cls._validate_not_terminal(execution)
        if execution.status != 'PENDING' and execution.status != 'SNOOZED':
            raise ValidationError(f"Cannot start execution from status: {execution.status}")

        now = timezone.now()
        execution.status = 'IN_PROGRESS'
        execution.actual_start = now
        execution.last_resumed_at = now
        execution.save()
        return execution

    @classmethod
    @transaction.atomic
    def pause(cls, execution: RoutineExecution) -> RoutineExecution:
        cls._validate_not_terminal(execution)
        if execution.status != 'IN_PROGRESS':
            raise ValidationError(f"Cannot pause execution from status: {execution.status}")

        now = timezone.now()
        if execution.last_resumed_at:
            delta = now - execution.last_resumed_at
            execution.duration_minutes += int(delta.total_seconds() // 60)
            execution.last_resumed_at = None

        execution.status = 'PAUSED'
        execution.save()
        return execution

    @classmethod
    @transaction.atomic
    def resume(cls, execution: RoutineExecution) -> RoutineExecution:
        cls._validate_not_terminal(execution)
        if execution.status != 'PAUSED':
            raise ValidationError(f"Cannot resume execution from status: {execution.status}")

        now = timezone.now()
        execution.status = 'IN_PROGRESS'
        execution.last_resumed_at = now
        execution.save()
        return execution

    @classmethod
    @transaction.atomic
    def complete(cls, execution: RoutineExecution) -> RoutineExecution:
        cls._validate_not_terminal(execution)
        
        # We can complete from IN_PROGRESS or PAUSED (or even PENDING if doing it instantly)
        now = timezone.now()
        
        # Add any remaining duration if it was in progress
        if execution.status == 'IN_PROGRESS' and execution.last_resumed_at:
            delta = now - execution.last_resumed_at
            execution.duration_minutes += int(delta.total_seconds() // 60)
            
        execution.status = 'COMPLETED'
        if not execution.actual_start:
            execution.actual_start = now
        execution.actual_end = now
        execution.last_resumed_at = None
        execution.save()
        return execution

    @classmethod
    @transaction.atomic
    def omit(cls, execution: RoutineExecution) -> RoutineExecution:
        cls._validate_not_terminal(execution)
        
        execution.status = 'OMITTED'
        execution.last_resumed_at = None
        execution.save()
        return execution

    @classmethod
    @transaction.atomic
    def snooze(cls, execution: RoutineExecution, minutes: int = 15) -> RoutineExecution:
        cls._validate_not_terminal(execution)
        if execution.status not in ['PENDING', 'SNOOZED']:
            raise ValidationError(f"Cannot snooze execution from status: {execution.status}")

        now = timezone.now()
        execution.status = 'SNOOZED'
        # Shift the scheduled times
        execution.scheduled_start = execution.scheduled_start + timedelta(minutes=minutes)
        execution.scheduled_end = execution.scheduled_end + timedelta(minutes=minutes)
        execution.save()
        return execution
