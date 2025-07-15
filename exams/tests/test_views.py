from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from users.models import CustomUser
from teachers.models import Teacher
from exams.models import Exam, Question, ExamSession
from datetime import date

class SubmitAnswerTest(APITestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(username='stud', email='s@x.com', password='pass', role='Student')
        self.teacher_user = CustomUser.objects.create_user(username='teach', email='t@x.com', password='pass', role='Teacher')
        self.teacher = Teacher.objects.create(user=self.teacher_user, first_name='T', last_name='Each', subject_specialization='Math', employee_id='EMP999', date_of_joining=date.today(), status='Active')
        self.exam = Exam.objects.create(teacher=self.teacher, title='Math Exam', description='Basics')
        self.question = Question.objects.create(exam=self.exam, text='5 + 5 = ?', option_a='9', option_b='10', option_c='11', option_d='12', correct_answer='B')
        self.session = ExamSession.objects.create(student=self.student, exam=self.exam)

        refresh = RefreshToken.for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_submit_valid_answer(self):
        data = [{
            "question": self.question.id,
            "selected_answer": "B"
        }]
        response = self.client.post('/api/submit-answer/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['correct_answers'], 1)

class StartExamTest(APITestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(username='stud2', email='s2@x.com', password='pass', role='Student')
        self.teacher_user = CustomUser.objects.create_user(username='teach2', email='t2@x.com', password='pass', role='Teacher')
        self.teacher = Teacher.objects.create(user=self.teacher_user, first_name='T', last_name='Each', subject_specialization='Math', employee_id='EMP998', date_of_joining=date.today(), status='Active')
        self.exam = Exam.objects.create(teacher=self.teacher, title='Algebra', description='Simple Algebra')

        refresh = RefreshToken.for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_start_exam_first_time(self):
        response = self.client.post(f'/api/start-exam/{self.exam.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Exam started', response.data['message'])
