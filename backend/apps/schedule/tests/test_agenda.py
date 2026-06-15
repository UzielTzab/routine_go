import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.routines.models import Category, RoutineTemplate, RoutineScheduleRule
from apps.executions.models import RoutineExecution

class ScheduleAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='schedule_user', password='password123')
        self.category = Category.objects.get(code='hygiene')
        
        self.routine1 = RoutineTemplate.objects.create(
            user=self.user, category=self.category, title='Morning check', default_duration_minutes=15
        )
        
        # Create a rule for TODAY
        now = timezone.now()
        self.today_str = str(now.weekday())
        
        RoutineScheduleRule.objects.create(
            routine=self.routine1,
            days_of_week=self.today_str,
            start_time=datetime.time(8, 0)
        )
        
        self.routine2 = RoutineTemplate.objects.create(
            user=self.user, category=self.category, title='Not today'
        )
        # Create a rule for a day that is NOT today
        not_today = str((now.weekday() + 1) % 7)
        RoutineScheduleRule.objects.create(
            routine=self.routine2,
            days_of_week=not_today,
            start_time=datetime.time(10, 0)
        )

    def test_get_today_schedule(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('schedule-today')
        
        # Primer llamado: debe crear la ejecución
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        execution = response.data[0]
        self.assertEqual(execution['routine']['title'], 'Morning check')
        self.assertEqual(execution['status'], 'PENDING')
        self.assertEqual(execution['duration_minutes'], 15)
        
        # Validar en base de datos
        self.assertEqual(RoutineExecution.objects.count(), 1)
        
        # Segundo llamado: no debe duplicar la ejecución
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(RoutineExecution.objects.count(), 1)
