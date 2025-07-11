from django.test import TestCase
from users.models import CustomUser

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='Teacher',
            phone_number='9876543210'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.role, 'Teacher')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role='Admin'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, 'Admin')
