from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from teachers.models import Teacher
from rest_framework.permissions import SAFE_METHODS

# For CSV export
from django.http import HttpResponse
import csv

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from users.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import csv
from io import TextIOWrapper


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
        user = self.request.user
        if user.is_authenticated and user.role == 'Student' and self.request.method not in SAFE_METHODS:

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
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # CSV Export Functionality
    @action(detail=False, methods=['get'], url_path='export-csv')
    def export_students_csv(self, request):
        user = request.user

        if user.role == 'Admin':
            students = Student.objects.all()
        elif user.role == 'Teacher':
            try:
                teacher = Teacher.objects.get(user=user)
                students = Student.objects.filter(assigned_teacher=teacher)
            except Teacher.DoesNotExist:
                return Response({'detail': 'Teacher not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

     
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Roll No',
            'Class', 'Date of Birth', 'Admission Date', 'Status', 'Assigned Teacher'
        ])

        for student in students:
            writer.writerow([
                student.id,
                student.first_name,
                student.last_name,
                student.user.email if student.user else '',
                student.user.phone_number if student.user else '',
                student.roll_number,
                student.student_class,
                student.date_of_birth,
                student.admission_date,
                student.status,
                student.assigned_teacher.user.username if student.assigned_teacher else ''
            ])

        return response



class StudentCSVImportView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        user = request.user

        if user.role not in ['Admin', 'Teacher']:
            return Response({"error": "Only Admins and Teachers can import students."}, status=403)

        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = TextIOWrapper(csv_file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        for index, row in enumerate(reader, start=1):
            try:
                validate_password(row['password'])

                if CustomUser.objects.filter(username=row['username']).exists():
                    errors.append(f"Row {index}: Username '{row['username']}' already exists.")
                    continue

                if CustomUser.objects.filter(email=row['email']).exists():
                    errors.append(f"Row {index}: Email '{row['email']}' already registered.")
                    continue

                user = CustomUser.objects.create_user(
                    username=row['username'],
                    email=row['email'],
                    password=row['password'],
                    phone_number=row['phone_number'],
                    role='Student'
                )

                Student.objects.create(
                    user=user,
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    roll_number=row['roll_number'],
                    student_class=row['student_class'],
                    date_of_birth=row['date_of_birth'],
                    admission_date=row['admission_date'],
                    status=row['status'],
                    assigned_teacher_id=row['assigned_teacher'],
                )

                created_count += 1

            except ValidationError as e:
                errors.append(f"Row {index}: {str(e)}")
            except Exception as e:
                errors.append(f"Row {index}: Unexpected error: {str(e)}")

        return Response({
            "message": f"{created_count} students created successfully.",
            "errors": errors
        }, status=201 if created_count > 0 else 400)

