from django.test import TestCase
from students.serializers import StudentSerializer
from users.models import CustomUser
from teachers.models import Teacher
from datetime import date

class StudentSerializerTest(TestCase):
    def setUp(self):
        self.teacher_user = CustomUser.objects.create_user(
            username='teacher1',
            email='teacher@example.com',
            phone_number='1112223333',
            password='pass1234',
            role='Teacher'
        )
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            date_of_joining=date(2020, 1, 1)
        )

    def test_student_serializer_valid_data(self):
        data = {
            "username": "student1",
            "password": "StrongPass123",
            "email": "alice@example.com",
            "phone_number": "9998887777",
            "first_name": "Alice",
            "last_name": "Wonder",
            "roll_number": "R100",
            "student_class": "10A",
            "date_of_birth": "2005-01-01",
            "admission_date": "2020-06-01",
            "status": "Active",
            "assigned_teacher": self.teacher.id
        }


        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        student = serializer.save()

        self.assertEqual(student.first_name, "Alice")
        self.assertEqual(student.user.username, "student1")
        self.assertEqual(student.user.email, "alice@example.com")
        self.assertEqual(student.user.phone_number, "9998887777")


    def test_student_serializer_missing_username(self):
        data = {
        
            "password": "StrongPass123",
            "email": "alice@example.com",
            "phone_number": "9998887777",
            "first_name": "Alice",
            "last_name": "Wonder",
            "roll_number": "R1001",
            "student_class": "10A",
            "date_of_birth": "2005-01-01",
            "admission_date": "2020-06-01",
            "status": "Active",
            "assigned_teacher": self.teacher.id
        }
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_student_serializer_invalid_phone_number(self):
        data = {
            "username": "student2",
            "password": "StrongPass123",
            "email": "bob@example.com",
            "phone_number": "123",  # Invalid
            "first_name": "Bob",
            "last_name": "Builder",
            "roll_number": "R1002",
            "student_class": "9B",
            "date_of_birth": "2006-02-01",
            "admission_date": "2021-06-01",
            "status": "Active",
            "assigned_teacher": self.teacher.id
        }
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone_number', serializer.errors)

    def test_student_serializer_invalid_dates(self):
        data = {
            "username": "student3",
            "password": "StrongPass123",
            "email": "charlie@example.com",
            "phone_number": "9997776666",
            "first_name": "Charlie",
            "last_name": "Day",
            "roll_number": "R1003",
            "student_class": "11C",
            "date_of_birth": "2020-01-01",
            "admission_date": "2019-01-01",  # Invalid: before DOB
            "status": "Active",
            "assigned_teacher": self.teacher.id
        }
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)



