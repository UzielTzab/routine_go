from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User

class CookieAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test@uzielos.com', password='password123')
        
    def test_token_obtain_sets_cookies(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'test@uzielos.com', 'password': 'password123'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se mandan las cookies
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
        
        access_cookie = response.cookies['access_token']
        self.assertTrue(access_cookie['httponly'])
        self.assertEqual(access_cookie['samesite'], 'Lax')

    def test_token_refresh_reads_from_cookie(self):
        # 1. Login para obtener el refresh_token
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'test@uzielos.com', 'password': 'password123'})
        refresh_token = response.cookies['refresh_token'].value
        
        # 2. Refrescar token pasándolo SOLO en cookies
        refresh_url = reverse('token_refresh')
        self.client.cookies['refresh_token'] = refresh_token
        refresh_response = self.client.post(refresh_url, {})
        
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', refresh_response.cookies)
        
    def test_logout_deletes_cookies(self):
        url = reverse('logout')
        # Seteamos fake cookies para ver si las elimina
        self.client.cookies['access_token'] = 'fake_access'
        self.client.cookies['refresh_token'] = 'fake_refresh'
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        access_cookie = response.cookies.get('access_token')
        refresh_cookie = response.cookies.get('refresh_token')
        
        # En Django test client, cuando se borra una cookie, su max-age es 0 (o expires en el pasado) y el value está vacío.
        self.assertEqual(access_cookie.value, '')
        self.assertEqual(refresh_cookie.value, '')

    def test_register_user(self):
        register_url = reverse('register')
        data = {
            'email': 'newuser@uzielos.com',
            'password': 'strongpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@uzielos.com').exists())
        
        # Verify tokens returned and cookies set
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
