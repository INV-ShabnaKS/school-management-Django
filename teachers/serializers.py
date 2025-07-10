from rest_framework import serializers
from .models import Teacher
from users.models import CustomUser
from django.core.validators import RegexValidator
from datetime import date
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)

class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    email = serializers.EmailField(source='user.email')
    phone_number = serializers.CharField(validators=[phone_validator], source='user.phone_number')

    def validate_password(self, value):
        try:
            validate_password(value)  
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
        
    class Meta:
        model = Teacher
        fields = [
            'id',
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

    def validate(self, data):
        email = data.get('user', {}).get('email')
        username = data.get('username')
        employee_id = data.get('employee_id')
        date_of_joining = data.get('date_of_joining')

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'This username is already taken.'})
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email is already registered.'})
        if Teacher.objects.filter(employee_id=employee_id).exists():
            raise serializers.ValidationError({'employee_id': 'This employee ID is already assigned.'})
        if date_of_joining and date_of_joining > date.today():
            raise serializers.ValidationError({'date_of_joining': 'Joining date cannot be in the future.'})
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        phone_number = validated_data.pop('phone_number')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            role='Teacher'
        )

        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)

        user = instance.user
        if 'username' in user_data:
            user.username = user_data['username']
        if 'email' in user_data:
            new_email = user_data['email']
            if CustomUser.objects.exclude(pk=user.pk).filter(email=new_email).exists():
                raise serializers.ValidationError({'email': 'Email already in use.'})
            user.email = new_email
        if 'phone_number' in user_data:
            user.phone_number = user_data['phone_number']
        if password:
            user.set_password(password)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
