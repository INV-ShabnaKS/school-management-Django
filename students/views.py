from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from teachers.models import Teacher


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
   
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Student.objects.all()
        elif user.role == 'Teacher':
            try:
                teacher = Teacher.objects.get(username=username) 
                return Student.objects.filter(assigned_teacher=teacher)
            except Teacher.DoesNotExist:
                return Student.objects.none()
        else:
            return Student.objects.filter(user=user)

    def get_permissions(self):
       
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
         
            if not (self.request.user.is_staff or self.request.user.role == 'Teacher'):
                return [IsAuthenticated()]  
        return [IsAuthenticated()]

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
