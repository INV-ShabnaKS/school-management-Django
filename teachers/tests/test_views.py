from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from teachers.models import Teacher
from datetime import date

class TeacherViewSetTest(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass', role='Admin'
        )
        self.non_admin = CustomUser.objects.create_user(
            username='user', email='user@example.com', password='userpass', role='Teacher'
        )
        self.teacher = Teacher.objects.create(
            user=self.non_admin,
            first_name='John',
            last_name='Doe',
            subject_specialization='Math',
            employee_id='EMP001',
            date_of_joining=date.today(),
            status='Active'
        )

    def get_auth_header(self, user):
        refresh = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'}

    def test_admin_can_export_csv(self):
        response = self.client.get('/api/teachers/export-csv/', **self.get_auth_header(self.admin))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('teachers.csv', response['Content-Disposition'])

    def test_non_admin_cannot_export_csv(self):
        response = self.client.get('/api/teachers/export-csv/', **self.get_auth_header(self.non_admin))
        self.assertEqual(response.status_code, 403)

    def test_non_admin_cannot_create_teacher(self):
        payload = {
            "username": "newteacher",
            "password": "Test12345",
            "email": "new@teacher.com",
            "phone_number": "1234567890",
            "first_name": "New",
            "last_name": "Teacher",
            "subject_specialization": "Science",
            "employee_id": "EMP999",
            "date_of_joining": str(date.today()),
            "status": "Active"
        }

        response = self.client.post('/api/teachers/', payload, **self.get_auth_header(self.non_admin))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_teacher(self):
        payload = {
            "username": "newteacher",
            "password": "Test12345",
            "email": "new@teacher.com",
            "phone_number": "9876543210",
            "first_name": "New",
            "last_name": "Teacher",
            "subject_specialization": "Biology",
            "employee_id": "EMP888",
            "date_of_joining": str(date.today()),
            "status": "Active"
        }

        response = self.client.post('/api/teachers/', payload, **self.get_auth_header(self.admin))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], 'New')
        self.assertEqual(response.data['subject_specialization'], 'Biology')

    