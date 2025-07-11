from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
import csv

from .models import Teacher
from .serializers import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Only admin can add teachers.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Only admin can update teachers.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Only admin can delete teachers.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    # CSV Export Functionality
    @action(detail=False, methods=['get'], url_path='export-csv')
    def export_teachers_csv(self, request):
       
        if not request.user.is_staff:
            return Response({'detail': 'Only admin can export teacher data.'}, status=status.HTTP_403_FORBIDDEN)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="teachers.csv"'

        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Employee ID',
            'Subject Specialization', 'Date of Joining', 'Status'
        ])

        
        for teacher in Teacher.objects.all():
            writer.writerow([
                teacher.id,
                teacher.first_name,
                teacher.last_name,
                teacher.user.email if teacher.user else '',
                teacher.user.phone_number if teacher.user else '',
                teacher.employee_id,
                teacher.subject_specialization,
                teacher.date_of_joining,
                teacher.status,
            ])

        return response
