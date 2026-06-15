from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from apps.accounts.models import User
from apps.routines.models import Category, RoutineTemplate
from apps.executions.models import RoutineExecution
from apps.notifications.models import Notification
from apps.executions.tasks import check_expired_executions_task, prepare_upcoming_notifications_task

class CeleryTasksTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test@uzielos.com', password='password123')
        self.category, _ = Category.objects.get_or_create(code='hygiene', defaults={'name':'Hygiene', 'color_code':'#fff'})
        self.routine = RoutineTemplate.objects.create(
            user=self.user,
            category=self.category,
            title="Brush Teeth",
            default_duration_minutes=5
        )

    def test_check_expired_executions_task(self):
        # Crear una ejecución que debió haber terminado hace 20 minutos
        past_time = timezone.now() - timedelta(minutes=20)
        execution = RoutineExecution.objects.create(
            user=self.user,
            routine=self.routine,
            scheduled_start=past_time - timedelta(minutes=5),
            scheduled_end=past_time,
            status='PENDING'
        )

        # Ejecutar tarea
        result = check_expired_executions_task()
        
        # Verificar estado
        execution.refresh_from_db()
        self.assertEqual(execution.status, 'OMITTED')
        self.assertIn("1 ejecuciones marcadas", result)

    def test_check_expired_executions_task_grace_period(self):
        # Crear una ejecución que terminó hace 10 minutos (dentro del grace period de 15)
        recent_past_time = timezone.now() - timedelta(minutes=10)
        execution = RoutineExecution.objects.create(
            user=self.user,
            routine=self.routine,
            scheduled_start=recent_past_time - timedelta(minutes=5),
            scheduled_end=recent_past_time,
            status='PENDING'
        )

        check_expired_executions_task()
        
        execution.refresh_from_db()
        self.assertEqual(execution.status, 'PENDING') # No debería cambiar

    def test_prepare_upcoming_notifications_task(self):
        # Crear una ejecución que empezará en 5 minutos
        future_time = timezone.now() + timedelta(minutes=5)
        execution = RoutineExecution.objects.create(
            user=self.user,
            routine=self.routine,
            scheduled_start=future_time,
            scheduled_end=future_time + timedelta(minutes=5),
            status='PENDING',
            notification_sent=False
        )

        result = prepare_upcoming_notifications_task()
        
        execution.refresh_from_db()
        self.assertTrue(execution.notification_sent)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertIn("1 notificaciones preparadas", result)

    def test_prepare_upcoming_notifications_task_ignores_far_future(self):
        # Crear ejecución en 20 minutos (más de los 10 mins de reminder)
        far_future_time = timezone.now() + timedelta(minutes=20)
        execution = RoutineExecution.objects.create(
            user=self.user,
            routine=self.routine,
            scheduled_start=far_future_time,
            scheduled_end=far_future_time + timedelta(minutes=5),
            status='PENDING',
            notification_sent=False
        )

        prepare_upcoming_notifications_task()
        
        execution.refresh_from_db()
        self.assertFalse(execution.notification_sent)
        self.assertEqual(Notification.objects.count(), 0)
