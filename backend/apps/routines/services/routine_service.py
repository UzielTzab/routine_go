from django.db import transaction
from ..models import RoutineTemplate, RoutineScheduleRule

@transaction.atomic
def create_routine_with_rules(user, routine_data, rules_data):
    routine_data.pop('schedule_rules', None)
    routine = RoutineTemplate.objects.create(user=user, **routine_data)
    for rule_data in rules_data:
        RoutineScheduleRule.objects.create(routine=routine, **rule_data)
    return routine

@transaction.atomic
def update_routine_with_rules(routine_instance, routine_data, rules_data=None):
    routine_data.pop('schedule_rules', None)
    for key, value in routine_data.items():
        setattr(routine_instance, key, value)
    routine_instance.save()
    
    if rules_data is not None:
        routine_instance.schedule_rules.all().delete()
        for rule_data in rules_data:
            RoutineScheduleRule.objects.create(routine=routine_instance, **rule_data)
            
    return routine_instance
