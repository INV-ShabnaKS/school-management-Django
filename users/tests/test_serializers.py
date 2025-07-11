from django.test import TestCase
from users.serializers import RegisterSerializer
from users.models import CustomUser

class RegisterSerializerTest(TestCase):
    def test_valid_data_creates_user(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone_number': '1234567890',
            'role': 'Student',
            'password': 'strongpass123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.role, 'Student')
        self.assertTrue(user.check_password('strongpass123'))

    def test_missing_fields_fails(self):
        data = {
            'username': '',
            'email': 'invalid@example.com',
            'role': 'Student',
            'password': 'pass'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
