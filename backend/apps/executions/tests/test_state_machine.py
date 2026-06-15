import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.routines.models import Category, RoutineTemplate
from apps.executions.models import RoutineExecution
from apps.executions.services.state_machine import ExecutionStateMachineService
from rest_framework.exceptions import ValidationError

class StateMachineServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(code='test', name='Test Category', color_code='#000000')
        self.routine = RoutineTemplate.objects.create(user=self.user, category=self.category, title='Test Routine')
        self.execution = RoutineExecution.objects.create(
            user=self.user,
            routine=self.routine,
            scheduled_start=timezone.now(),
            scheduled_end=timezone.now() + datetime.timedelta(minutes=15),
            status='PENDING'
        )

    def test_start_execution(self):
        ExecutionStateMachineService.start(self.execution)
        self.assertEqual(self.execution.status, 'IN_PROGRESS')
        self.assertIsNotNone(self.execution.actual_start)
        self.assertIsNotNone(self.execution.last_resumed_at)

    def test_invalid_start_execution(self):
        self.execution.status = 'COMPLETED'
        self.execution.save()
        with self.assertRaises(ValidationError):
            ExecutionStateMachineService.start(self.execution)

    def test_pause_and_resume_execution(self):
        ExecutionStateMachineService.start(self.execution)
        
        # Simular que pasó tiempo
        self.execution.last_resumed_at -= datetime.timedelta(minutes=10)
        self.execution.save()
        
        ExecutionStateMachineService.pause(self.execution)
        self.assertEqual(self.execution.status, 'PAUSED')
        self.assertEqual(self.execution.duration_minutes, 10)
        self.assertIsNone(self.execution.last_resumed_at)
        
        ExecutionStateMachineService.resume(self.execution)
        self.assertEqual(self.execution.status, 'IN_PROGRESS')
        self.assertIsNotNone(self.execution.last_resumed_at)

    def test_complete_execution(self):
        ExecutionStateMachineService.start(self.execution)
        self.execution.last_resumed_at -= datetime.timedelta(minutes=5)
        self.execution.save()
        
        ExecutionStateMachineService.complete(self.execution)
        self.assertEqual(self.execution.status, 'COMPLETED')
        self.assertEqual(self.execution.duration_minutes, 5)
        self.assertIsNotNone(self.execution.actual_end)

    def test_omit_execution(self):
        ExecutionStateMachineService.omit(self.execution)
        self.assertEqual(self.execution.status, 'OMITTED')

    def test_terminal_states_protection(self):
        ExecutionStateMachineService.start(self.execution)
        ExecutionStateMachineService.complete(self.execution)
        
        with self.assertRaises(ValidationError):
            ExecutionStateMachineService.start(self.execution)
            
        with self.assertRaises(ValidationError):
            ExecutionStateMachineService.resume(self.execution)

class StateMachineAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(code='api', name='API Category', color_code='#000000')
        self.routine = RoutineTemplate.objects.create(user=self.user, category=self.category, title='API Routine')
        self.execution = RoutineExecution.objects.create(
            user=self.user,
            routine=self.routine,
            scheduled_start=timezone.now(),
            scheduled_end=timezone.now() + datetime.timedelta(minutes=15),
            status='PENDING'
        )

    def test_start_endpoint(self):
        url = reverse('execution-start', kwargs={'id': self.execution.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'IN_PROGRESS')

    def test_invalid_transition_endpoint(self):
        url = reverse('execution-pause', kwargs={'id': self.execution.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
