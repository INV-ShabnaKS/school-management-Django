from rest_framework import serializers
from .models import Student
from users.models import CustomUser

class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(source='user.username',write_only=True)


    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number',
                  'roll_number', 'student_class', 'date_of_birth', 'admission_date',
                  'status', 'assigned_teacher', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('username')  
        print("usernaem", username)
        email = validated_data.get('email')

        if CustomUser.objects.filter(username=username).exists():
            print("bla")
            raise serializers.ValidationError({'username': 'This username is already taken.'})
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email is already registered.'})

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='Student'
        )

        student = Student.objects.create(user=user, **validated_data)
        return student


