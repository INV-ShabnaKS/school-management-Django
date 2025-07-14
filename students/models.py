from django.db import models
from users.models import CustomUser
from teachers.models import Teacher

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, unique=True)
    student_class = models.CharField(max_length=50)  # Class/Grade
    date_of_birth = models.DateField()
    admission_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
 
    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)