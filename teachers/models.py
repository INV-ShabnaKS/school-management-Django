from django.db import models

class Teacher(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    username = models.CharField(max_length=150, default='temp_teacher') 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    subject_specialization = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    date_of_joining = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject_specialization}"
