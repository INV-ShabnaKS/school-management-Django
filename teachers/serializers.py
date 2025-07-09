from rest_framework import serializers
from .models import Teacher
from users.models import CustomUser
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)

class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True) 
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(validators=[phone_validator])

    class Meta:
        model = Teacher
        fields = [
            'username',            
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'subject_specialization',
            'employee_id',
            'date_of_joining',
            'status',
            'password',
        ]

    def create(self, validated_data):
        uname = validated_data.pop('username')
        pwd   = validated_data.pop('password')
        teacher = Teacher.objects.create(**validated_data)

       
        CustomUser.objects.create_user(
            username=uname,
            email=teacher.email,
            password=pwd,
            role='Teacher'
        )

        return teacher
