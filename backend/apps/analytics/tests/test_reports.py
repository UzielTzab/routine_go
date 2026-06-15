from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from apps.accounts.models import User
from apps.routines.models import Category, RoutineTemplate
from apps.executions.models import RoutineExecution
from apps.analytics.services.reports import ReportsService

class ReportsServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reports@uzielos.com', password='password123')
        self.cat_sleep, _ = Category.objects.get_or_create(code='sleep', defaults={'name':'Sleep', 'color_code':'#000'})
        self.cat_focus, _ = Category.objects.get_or_create(code='focus', defaults={'name':'Focus', 'color_code':'#111'})
        self.routine_sleep = RoutineTemplate.objects.create(user=self.user, category=self.cat_sleep, title="Sleep", default_duration_minutes=480)
        self.routine_focus = RoutineTemplate.objects.create(user=self.user, category=self.cat_focus, title="Code", default_duration_minutes=120)

    def test_get_weekly_progress_no_data(self):
        now = timezone.now()
        progress = ReportsService.get_weekly_progress(self.user, now)
        self.assertEqual(len(progress), 7)
        for p in progress:
            self.assertEqual(p['compliance'], 0)

    def test_get_weekly_progress_mixed(self):
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        
        # 2 ejecuciones ayer, 1 completada, 1 omitida -> 50%
        RoutineExecution.objects.create(
            user=self.user, routine=self.routine_focus, status='COMPLETED', 
            scheduled_start=yesterday, scheduled_end=yesterday, actual_end=yesterday
        )
        RoutineExecution.objects.create(
            user=self.user, routine=self.routine_focus, status='OMITTED', 
            scheduled_start=yesterday, scheduled_end=yesterday
        )

        progress = ReportsService.get_weekly_progress(self.user, now)
        yesterday_data = next((p for p in progress if p['date'] == yesterday.date().isoformat()), None)
        self.assertIsNotNone(yesterday_data)
        self.assertEqual(yesterday_data['compliance'], 50)

    def test_get_heatmap_90_days(self):
        now = timezone.now()
        target_date = now - timedelta(days=45)
        
        RoutineExecution.objects.create(
            user=self.user, routine=self.routine_focus, status='COMPLETED', 
            scheduled_start=target_date, scheduled_end=target_date, actual_end=target_date
        )

        heatmap = ReportsService.get_heatmap_90_days(self.user, now)
        self.assertEqual(len(heatmap), 90)
        
        active_day = next((h for h in heatmap if h['date'] == target_date.date().isoformat()), None)
        self.assertTrue(active_day['active'])

    def test_get_hourly_compliance(self):
        now = timezone.now()
        
        # Crear en la hora 14 (2 PM) local
        target_time = now.replace(hour=14, minute=30, second=0)
        
        RoutineExecution.objects.create(
            user=self.user, routine=self.routine_focus, status='COMPLETED', 
            scheduled_start=target_time, scheduled_end=target_time, actual_end=target_time
        )
        
        hourly = ReportsService.get_hourly_compliance(self.user, now)
        self.assertEqual(len(hourly), 24)
        
        local_target_time = timezone.localtime(target_time)
        target_data = next((h for h in hourly if h['hour_24'] == local_target_time.hour), None)
        self.assertIsNotNone(target_data)
        self.assertEqual(target_data['count'], 1)

    def test_get_sleep_vs_focus(self):
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        
        RoutineExecution.objects.create(
            user=self.user, routine=self.routine_sleep, status='COMPLETED', 
            scheduled_start=yesterday, scheduled_end=yesterday, actual_end=yesterday,
            duration_minutes=480 # 8 horas
        )
        
        RoutineExecution.objects.create(
            user=self.user, routine=self.routine_focus, status='COMPLETED', 
            scheduled_start=yesterday, scheduled_end=yesterday, actual_end=yesterday,
            duration_minutes=120 # 2 horas
        )
        
        res = ReportsService.get_sleep_vs_focus(self.user, now)
        self.assertEqual(len(res), 7)
        
        yesterday_data = next((d for d in res if d['day'] == yesterday.strftime('%a')), None)
        self.assertIsNotNone(yesterday_data)
        self.assertEqual(yesterday_data['sleep_hours'], 8.0)
        self.assertEqual(yesterday_data['focus_hours'], 2.0)
