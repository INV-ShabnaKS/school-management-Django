from django.test import TestCase
from users.models import CustomUser
from teachers.models import Teacher
from students.models import Student
from datetime import date

class StudentModelTest(TestCase):
    def setUp(self):
       
        self.teacher_user = CustomUser.objects.create_user(
            username='teacheruser',
            email='teacher@example.com',
            phone_number='1234567890',
            password='pass1234',
            role='Teacher'
        )

        
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            date_of_joining=date(2020, 6, 1) 
        )

        
        self.student_user = CustomUser.objects.create_user(
            username='studentuser',
            email='student@example.com',
            phone_number='9876543210',
            password='pass1234',
            role='Student'
        )

    def test_student_creation(self):
       
        student = Student.objects.create(
            user=self.student_user,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone_number='9876543210',
            roll_number='S123',
            student_class='10A',
            date_of_birth=date(2005, 5, 15),
            admission_date=date(2021, 6, 1),
            status='Active',
            assigned_teacher=self.teacher
        )

       
        self.assertEqual(student.first_name, 'John')     
        self.assertEqual(student.last_name, 'Doe')       
        self.assertEqual(student.roll_number, 'S123')    
        self.assertEqual(student.student_class,'10A')    
