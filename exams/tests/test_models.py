from django.test import TestCase
from exams.models import Exam, Question, StudentAnswer, ExamSession
from users.models import CustomUser
from teachers.models import Teacher
from datetime import date
from django.utils import timezone

class ExamModelTest(TestCase):
    def setUp(self):
        self.teacher_user = CustomUser.objects.create_user(username='teach1', email='t1@example.com', password='pass', role='Teacher')
        self.teacher = Teacher.objects.create(user=self.teacher_user, first_name='T', last_name='One', subject_specialization='Math', employee_id='EMP001', date_of_joining=date.today(), status='Active')
        self.exam = Exam.objects.create(teacher=self.teacher, title='Unit Test 1', description='Basic Test')

    def test_exam_str(self):
        self.assertEqual(str(self.exam), 'Unit Test 1')

class QuestionModelTest(TestCase):
    def setUp(self):
        teacher_user = CustomUser.objects.create_user(username='teach2', email='t2@example.com', password='pass', role='Teacher')
        teacher = Teacher.objects.create(user=teacher_user, first_name='T', last_name='Two', subject_specialization='Science', employee_id='EMP002', date_of_joining=date.today(), status='Active')
        self.exam = Exam.objects.create(teacher=teacher, title='Quiz', description='Some desc')
        self.question = Question.objects.create(exam=self.exam, text='2 + 2 = ?', option_a='3', option_b='4', option_c='5', option_d='6', correct_answer='B')

    def test_question_str(self):
        self.assertIn('2 + 2', str(self.question))

class StudentAnswerModelTest(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(username='stud1', email='s@example.com', password='pass', role='Student')
        teacher_user = CustomUser.objects.create_user(username='teach3', email='t3@example.com', password='pass', role='Teacher')
        teacher = Teacher.objects.create(user=teacher_user, first_name='T', last_name='Three', subject_specialization='English', employee_id='EMP003', date_of_joining=date.today(), status='Active')
        self.exam = Exam.objects.create(teacher=teacher, title='Grammar Test', description='English')
        self.question = Question.objects.create(exam=self.exam, text='Choose the correct form', option_a='go', option_b='went', option_c='going', option_d='gone', correct_answer='B')

    def test_answer_correctness(self):
        ans = StudentAnswer.objects.create(student=self.student, question=self.question, selected_answer='B')
        self.assertTrue(ans.is_correct)

    def test_answer_incorrectness(self):
        ans = StudentAnswer.objects.create(student=self.student, question=self.question, selected_answer='C')
        self.assertFalse(ans.is_correct)

class ExamSessionModelTest(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(username='stud2', email='s2@example.com', password='pass', role='Student')
        teacher_user = CustomUser.objects.create_user(username='teach4', email='t4@example.com', password='pass', role='Teacher')
        teacher = Teacher.objects.create(user=teacher_user, first_name='T', last_name='Four', subject_specialization='History', employee_id='EMP004', date_of_joining=date.today(), status='Active')
        self.exam = Exam.objects.create(teacher=teacher, title='History Test', description='WW2')
        self.session = ExamSession.objects.create(student=self.student, exam=self.exam)

    def test_time_exceeded_false(self):
        self.assertFalse(self.session.is_time_exceeded())

    def test_str_method(self):
        self.assertIn(self.student.username, str(self.session))
