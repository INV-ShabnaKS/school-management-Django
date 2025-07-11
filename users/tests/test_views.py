from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class UserAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='Teacher',
            phone_number='1234567890'
        )

    def test_login_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['role'], 'Teacher')

    def test_login_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/logout/', {"refresh": str(refresh)}, format='json')
        self.assertEqual(response.status_code, 205)
