from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, QuestionViewSet, SubmitAnswerView , StudentScoreView , start_exam


router = DefaultRouter()
router.register('exams', ExamViewSet, basename='exam')
router.register('questions', QuestionViewSet, basename='question')


urlpatterns = [
    path('', include(router.urls)),
    path('submit-answer/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('student-score', StudentScoreView.as_view(), name='student-score'),
    path('start/<int:exam_id>/', start_exam, name='start-exam'),
]
