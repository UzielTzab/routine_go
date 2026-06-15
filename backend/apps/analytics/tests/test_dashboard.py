from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.routines.models import Category, RoutineTemplate, RoutineScheduleRule
from apps.executions.models import RoutineExecution
from apps.analytics.services.dashboard_service import DashboardService

class DashboardServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test@uzielos.com', password='password123')
        self.category = Category.objects.create(code='health', name='Health', color_code='#000000')
        self.routine = RoutineTemplate.objects.create(user=self.user, category=self.category, title='Drink Water')
        
        now = timezone.now()
        RoutineScheduleRule.objects.create(
            routine=self.routine,
            days_of_week=str(now.weekday()),
            start_time=now.time()
        )

    def test_current_streak_zero(self):
        streak = DashboardService.get_current_streak(self.user)
        self.assertEqual(streak, 0)

    def test_current_streak_one(self):
        # Creamos una ejecución completada hoy
        RoutineExecution.objects.create(
            user=self.user,
            routine=self.routine,
            scheduled_start=timezone.now(),
            scheduled_end=timezone.now() + timedelta(minutes=15),
            actual_end=timezone.now(),
            status='COMPLETED'
        )
        streak = DashboardService.get_current_streak(self.user)
        self.assertEqual(streak, 1)

    def test_daily_progress_and_up_next(self):
        # get_daily_progress generará la ejecución PENDING a través del agenda_service
        progress = DashboardService.get_daily_progress(self.user)
        self.assertEqual(len(progress), 1)
        self.assertEqual(progress[0]['category_code'], 'health')
        self.assertEqual(progress[0]['total'], 1)
        self.assertEqual(progress[0]['completed'], 0)
        self.assertEqual(progress[0]['percentage'], 0)

        up_next = DashboardService.get_up_next(self.user)
        self.assertIsNotNone(up_next)
        self.assertEqual(up_next['title'], 'Drink Water')

class DashboardAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test@uzielos.com', password='password123')
        
    def test_jwt_auth_and_dashboard(self):
        # Test JWT login
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'username': 'test@uzielos.com', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
        access_token = response.cookies.get('access_token').value
        self.client.cookies['access_token'] = access_token
        
        # Test Dashboard endpoint
        url = reverse('analytics-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('current_streak', response.data)
        self.assertIn('daily_progress', response.data)
        self.assertIn('up_next', response.data)
