from rest_framework import serializers
from .models import Category, RoutineTemplate, RoutineScheduleRule

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'code', 'name', 'color_code']

class RoutineScheduleRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineScheduleRule
        fields = ['id', 'days_of_week', 'start_time', 'reminder_minutes', 'timezone', 'auto_complete', 'active']

class RoutineTemplateSerializer(serializers.ModelSerializer):
    schedule_rules = RoutineScheduleRuleSerializer(many=True, required=False)

    class Meta:
        model = RoutineTemplate
        fields = ['id', 'category', 'title', 'instructions', 'default_duration_minutes', 'priority', 'active', 'schedule_rules', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        schedule_rules_data = validated_data.pop('schedule_rules', [])
        routine = RoutineTemplate.objects.create(**validated_data)
        for rule_data in schedule_rules_data:
            RoutineScheduleRule.objects.create(routine=routine, **rule_data)
        return routine
