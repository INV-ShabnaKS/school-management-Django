from django.db import models
from users.models import CustomUser

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject_specialization = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    date_of_joining = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject_specialization}"

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)