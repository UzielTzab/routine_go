from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.routines.models import Category, RoutineTemplate, RoutineScheduleRule

class RoutineAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.category = Category.objects.get(code='hygiene')
        
        self.routine1 = RoutineTemplate.objects.create(
            user=self.user1, category=self.category, title='Brush teeth'
        )

    def test_list_categories(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        codes = [c['code'] for c in response.data]
        self.assertIn('hygiene', codes)

    def test_list_routines_is_isolated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('routinetemplate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.client.force_authenticate(user=self.user2)
        response2 = self.client.get(url)
        self.assertEqual(len(response2.data), 0)

    def test_create_routine_with_rules(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('routinetemplate-list')
        data = {
            "category": self.category.id,
            "title": "Morning run",
            "schedule_rules": [
                {
                    "days_of_week": "1,2,3,4,5",
                    "start_time": "06:00:00"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoutineTemplate.objects.filter(user=self.user1).count(), 2)
        self.assertEqual(RoutineScheduleRule.objects.count(), 1)
