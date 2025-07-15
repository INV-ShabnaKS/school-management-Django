from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from .models import Exam, Question, StudentAnswer, ExamSession
from .serializers import ExamSerializer, QuestionTeacherSerializer, QuestionStudentSerializer, StudentAnswerSerializer
from teachers.models import Teacher
from users.models import CustomUser


class ExamViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Teacher':
            teacher = Teacher.objects.get(user=user)
            return Exam.objects.filter(teacher=teacher)
        elif user.role == 'Student':
            return Exam.objects.all()
        return Exam.objects.none()

    def perform_create(self, serializer):
        teacher = Teacher.objects.get(user=self.request.user)
        serializer.save(teacher=teacher)

    def get_permissions(self):
        if self.request.user.role == 'Student' and self.request.method not in ['GET', 'HEAD', 'OPTIONS']:
            self.permission_denied(
                self.request,
                message="Students can only view exams."
            )
        return super().get_permissions()


from .serializers import QuestionTeacherSerializer, QuestionStudentSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        exam_id = self.request.query_params.get('exam')  
        if user.role == 'Teacher':
            try:
                teacher = Teacher.objects.get(user=user)
                exams = Exam.objects.filter(teacher=teacher)
                return Question.objects.filter(exam__in=exams)
            except Teacher.DoesNotExist:
                return Question.objects.none()
        elif user.role == 'Student':
            if exam_id:
                return Question.objects.filter(exam__id=exam_id)
            return Question.objects.none()
        return Question.objects.none()

    def get_serializer_class(self):
        user = self.request.user
        if user.role == 'Teacher':
            return QuestionTeacherSerializer  
        return QuestionStudentSerializer      

    def perform_create(self, serializer):
        exam = serializer.validated_data['exam']
        user = self.request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            raise PermissionDenied("You are not a Teacher")
        if exam.teacher != teacher:
            raise PermissionDenied("You can only edit questions for your own exams")
        serializer.save()

    def get_permissions(self):
        if self.request.user.role == 'Student' and self.request.method not in ['GET', 'HEAD', 'OPTIONS']:
            self.permission_denied(
                self.request,
                message="Students can only view questions."
            )
        return super().get_permissions()



class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'Student':
            return Response({"detail": "Only students can submit answers"}, status=403)

        answers_data = request.data
        if not isinstance(answers_data, list):
            return Response({"detail": "Data must be a list of answers."}, status=400)

        if not answers_data:
            return Response({"detail": "No answers provided."}, status=400)

        first_question_id = answers_data[0].get('question')
        if not first_question_id:
            return Response({"error": "Missing question ID."}, status=400)

        try:
            question = Question.objects.get(id=first_question_id)
            exam = question.exam
        except Question.DoesNotExist:
            return Response({"error": "Invalid question ID."}, status=400)

        try:
            session = ExamSession.objects.get(student=user, exam=exam)
        except ExamSession.DoesNotExist:
            return Response({"error": "You haven't started this exam."}, status=400)

        if session.is_time_exceeded():
            return Response({"error": "Time exceeded. Cannot submit answers."}, status=403)

        if session.submitted:
            return Response({"error": "You have already submitted this exam."}, status=403)

        saved_answers = []
        for answer_data in answers_data:
            question_id = answer_data.get('question')
            selected_answer = answer_data.get('selected_answer')

            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                continue  

            answer, _ = StudentAnswer.objects.update_or_create(
                student=user,
                question=question,
                defaults={'selected_answer': selected_answer}
            )
            saved_answers.append(answer)

        
        session.submitted = True
        session.save()

        total = len(saved_answers)
        correct = sum(1 for ans in saved_answers if ans.is_correct)

        return Response({
            "message": "You’ve completed the exam.",
            "student": user.username,
            "exam": exam.title,
            "total_attempted": total,
            "correct_answers": correct,
            "score": f"{correct} / {total}"
        }, status=200)




class StudentScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'Student':
            return Response({"detail": "Only students can view scores."}, status=403)

        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response({"error": "exam_id is required in URL"}, status=400)

        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=404)

        try:
            session = ExamSession.objects.get(student=user, exam=exam)
        except ExamSession.DoesNotExist:
            return Response({"error": "You have not started this exam"}, status=404)

        if session.is_time_exceeded():
            return Response({"error": "Time exceeded. Cannot show score."}, status=403)

        answers = StudentAnswer.objects.filter(student=user, question__exam=exam)
        total = answers.count()
        correct = answers.filter(is_correct=True).count()

        return Response({
            "student": user.username,
            "exam": exam.title,
            "total_attempted": total,
            "correct_answers": correct,
            "score": f"{correct} / {total}"
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_exam(request, exam_id):
    user = request.user
    if user.role != 'Student':
        return Response({"detail": "Only students can start exams."}, status=403)

    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({"detail": "Exam not found."}, status=404)

    session, created = ExamSession.objects.get_or_create(student=user, exam=exam)

    if not created:
        if session.is_time_exceeded():
            session.started_at = timezone.now()
            session.save()
            return Response({"message": "Exam restarted. You have 5 minutes from now."})
        else:
            return Response({"detail": "You already started this exam."}, status=400)

    return Response({"message": "Exam started. You have 5 minutes to finish."})
