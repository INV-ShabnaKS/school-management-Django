from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from teachers.models import Teacher
from rest_framework.permissions import SAFE_METHODS



class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
   
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Student.objects.all()
        elif user.role == 'Teacher':
            try:
                teacher = Teacher.objects.get(user=user) 
                return Student.objects.filter(assigned_teacher=teacher)
            except Teacher.DoesNotExist:
                return Student.objects.none()
        else:
            return Student.objects.filter(user=user)

    def get_permissions(self):
        user= self.request.user
        if user.role == 'Student' and self.request.method not in SAFE_METHODS:
            self.permission_denied(
                self.request,
                message="Students are only allowed to view their own details."
            )

        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='assigned')
    def assigned(self, request):
       
        user = request.user
        if user.role == 'Teacher':
            qs = Student.objects.filter(assigned_teacher__user=user)
        elif user.is_staff:
            qs = Student.objects.all()
        else:
            return Response({"detail":"Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
