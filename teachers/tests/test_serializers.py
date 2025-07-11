from django.test import TestCase
from teachers.serializers import TeacherSerializer
from users.models import CustomUser
from teachers.models import Teacher
from datetime import date, timedelta

class TeacherSerializerTest(TestCase):

    def test_valid_teacher_data_creates_teacher(self):
        data = {
            "username": "testteacher",
            "password": "StrongPass123",
            "email": "teacher@example.com",
            "phone_number": "9876543210",
            "first_name": "Test",
            "last_name": "Teacher",
            "subject_specialization": "Math",
            "employee_id": "EMP123",
            "date_of_joining": str(date.today()),
            "status": "Active"
        }

        serializer = TeacherSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        teacher = serializer.save()
        self.assertEqual(teacher.first_name, "Test")
        self.assertEqual(teacher.user.email, "teacher@example.com")

    def test_future_date_of_joining_invalid(self):
        future_date = date.today() + timedelta(days=5)
        data = {
            "username": "futureteacher",
            "password": "StrongPass123",
            "email": "future@example.com",
            "phone_number": "9999999999",
            "first_name": "Future",
            "last_name": "Teacher",
            "subject_specialization": "Science",
            "employee_id": "EMP124",
            "date_of_joining": str(future_date),
            "status": "Active"
        }

        serializer = TeacherSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_of_joining', serializer.errors)

    def test_duplicate_username_fails(self):
        CustomUser.objects.create_user(
            username="duplicateuser",
            email="dup@example.com",
            phone_number="1234567890",
            password="somepass",
            role="Teacher"
        )

        data = {
            "username": "duplicateuser",  # already exists
            "password": "StrongPass123",
            "email": "new@example.com",
            "phone_number": "9876543210",
            "first_name": "Dup",
            "last_name": "User",
            "subject_specialization": "Bio",
            "employee_id": "EMP200",
            "date_of_joining": str(date.today()),
            "status": "Active"
        }

        serializer = TeacherSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
