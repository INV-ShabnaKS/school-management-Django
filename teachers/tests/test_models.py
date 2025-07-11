from django.test import TestCase
from teachers.models import Teacher
from users.models import CustomUser
from datetime import date


class TeacherModelTest(TestCase):
    def test_teacher_str_representation(self):
        user = CustomUser.objects.create_user(
            username='teacheruser',
            email='teacher@example.com',
            password='pass123',
            role='Teacher',
            phone_number='1234567890'
        )
        teacher = Teacher.objects.create(
            user=user,
            first_name='John',
            last_name='Doe',
            subject_specialization='Math',
            employee_id='EMP123',
            date_of_joining=date(2020, 1, 1),
            status='Active'
        )
        self.assertEqual(str(teacher), "John Doe - Math")
