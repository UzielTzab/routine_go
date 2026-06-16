import datetime
try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo
from django.utils import timezone
from apps.routines.models import RoutineScheduleRule
from apps.executions.models import RoutineExecution

def get_today_agenda(user):
    """
    Evaluates active rules for today based on the rule's local timezone, 
    lazily creates RoutineExecution instances if they don't exist,
    and returns a queryset of today's RoutineExecutions ordered by scheduled time.
    """
    rules = RoutineScheduleRule.objects.filter(
        routine__user=user,
        active=True,
        routine__active=True
    )
    
    executions_ids = []
    
    for rule in rules:
        try:
            rule_tz = zoneinfo.ZoneInfo(rule.timezone)
        except Exception:
            rule_tz = timezone.get_current_timezone()
            
        user_now = timezone.now().astimezone(rule_tz)
        today_weekday_str = str(user_now.weekday())
        
        days_list = [d.strip() for d in rule.days_of_week.split(',')]
        if today_weekday_str not in days_list:
            continue
            
        today_date = user_now.date()
        naive_dt = datetime.datetime.combine(today_date, rule.start_time)
        aware_dt = timezone.make_aware(naive_dt, rule_tz)
        
        duration_mins = rule.routine.default_duration_minutes
        aware_end_dt = aware_dt + datetime.timedelta(minutes=duration_mins)
        
        execution, _ = RoutineExecution.objects.get_or_create(
            user=user,
            routine=rule.routine,
            scheduled_start=aware_dt,
            defaults={
                'scheduled_end': aware_end_dt,
                'duration_minutes': duration_mins,
                'status': 'PENDING'
            }
        )
        executions_ids.append(execution.id)
        
    return RoutineExecution.objects.filter(id__in=executions_ids).order_by('scheduled_start')
