from rest_framework import serializers
from .models import Exam, Question, StudentAnswer

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class QuestionTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'exam', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']


class QuestionStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'exam', 'text', 'option_a', 'option_b', 'option_c', 'option_d']


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['id', 'student', 'question', 'selected_answer', 'is_correct']
        read_only_fields = ['is_correct']
