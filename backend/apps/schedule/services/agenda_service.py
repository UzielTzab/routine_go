import datetime
from django.utils import timezone
from apps.routines.models import RoutineScheduleRule
from apps.executions.models import RoutineExecution

def get_today_agenda(user):
    """
    Evaluates active rules for today, lazily creates RoutineExecution instances if they don't exist,
    and returns a queryset of today's RoutineExecutions ordered by scheduled time.
    """
    now = timezone.now()
    # Using python's weekday (0=Monday, 6=Sunday)
    # The days_of_week is stored as a string like "0,1,2,3,4,5,6"
    today_weekday_str = str(now.weekday())
    
    # 1. Get all active rules for the user that match today's weekday
    # Note: days_of_week might be a comma separated string
    rules = RoutineScheduleRule.objects.filter(
        routine__user=user,
        active=True,
        routine__active=True,
        days_of_week__contains=today_weekday_str
    )
    
    today_date = now.date()
    
    # 2. Lazily create missing executions
    for rule in rules:
        # Check if the weekday is exactly in the list
        days_list = [d.strip() for d in rule.days_of_week.split(',')]
        if today_weekday_str not in days_list:
            continue
            
        # Determine scheduled start and end
        # We combine today's date with the rule's start_time
        # Warning: For a full production app, timezone conversions should be applied here.
        # For Phase 2, we'll use naive/current timezone combinations.
        naive_dt = datetime.datetime.combine(today_date, rule.start_time)
        aware_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())
        
        # Calculate duration
        duration_mins = rule.routine.default_duration_minutes
        aware_end_dt = aware_dt + datetime.timedelta(minutes=duration_mins)
        
        # Check if an execution already exists for this routine and scheduled start
        # Use get_or_create to lazily initialize
        RoutineExecution.objects.get_or_create(
            user=user,
            routine=rule.routine,
            scheduled_start=aware_dt,
            defaults={
                'scheduled_end': aware_end_dt,
                'duration_minutes': duration_mins,
                'status': 'PENDING'
            }
        )
        
    # 3. Return the day's executions ordered by scheduled_start
    start_of_day = timezone.make_aware(datetime.datetime.combine(today_date, datetime.time.min))
    end_of_day = timezone.make_aware(datetime.datetime.combine(today_date, datetime.time.max))
    
    return RoutineExecution.objects.filter(
        user=user,
        scheduled_start__range=(start_of_day, end_of_day)
    ).order_by('scheduled_start')
