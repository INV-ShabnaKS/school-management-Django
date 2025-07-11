from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from teachers.models import Teacher
from students.models import Student
from datetime import date

class StudentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

     
        self.teacher_user = CustomUser.objects.create_user(
            username='teacheruser',
            email='teacher@example.com',
            phone_number='1234567890',
            password='pass1234',
            role='Teacher'
        )

  
        self.other_user = CustomUser.objects.create_user(
            username='other',
            email='other@example.com',
            phone_number='2223334444',
            password='pass1234',
            role='Teacher'
        )

        
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            employee_id='EMP001',
            date_of_joining=date(2020, 6, 1)
        )

        self.other_teacher = Teacher.objects.create(
            user=self.other_user,
            employee_id='EMP002',
            date_of_joining=date(2020, 1, 1)
        )

       
        self.student1 = Student.objects.create(
            user=CustomUser.objects.create_user(
                username='student1',
                email='s1@example.com',
                phone_number='1111111111',
                password='pass',
                role='Student'
            ),
            first_name='John',
            last_name='Doe',
            roll_number='S1',
            student_class='10A',
            date_of_birth=date(2005, 1, 1),
            admission_date=date(2020, 6, 1),
            status='Active',
            assigned_teacher=self.teacher
        )

       
        self.student2 = Student.objects.create(
            user=CustomUser.objects.create_user(
                username='student2',
                email='s2@example.com',
                phone_number='2222222222',
                password='pass',
                role='Student'
            ),
            first_name='Jane',
            last_name='Smith',
            roll_number='S2',
            student_class='10B',
            date_of_birth=date(2006, 2, 2),
            admission_date=date(2021, 6, 1),
            status='Active',
            assigned_teacher=self.other_teacher
        )

    def test_teacher_can_see_only_their_assigned_students(self):
        
        self.client.force_authenticate(user=self.teacher_user)

       
        response = self.client.get('/api/students/assigned/')


        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)  
        self.assertEqual(response.data['results'][0]['first_name'], 'John')

    def test_export_students_csv(self):
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get('/api/students/export-csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('students.csv', response['Content-Disposition'])
        content = response.content.decode('utf-8')
        self.assertIn('John', content)  
        self.assertIn('Doe', content)   

    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/students/assigned/')
        self.assertEqual(response.status_code, 401)

