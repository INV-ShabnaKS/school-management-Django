from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,username,email,password=None, role=None,phone_number=None):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("users must have a Password")
        
        email=self.normalize_email(email)
        user=self.model(username=username, email=email, role=role,phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,password=None, role=None):
        
        user=self.create_user(username,email, password, role=role)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES=(
        ('Admin', 'Admin'),
        ('Teacher','Teacher'),
        ('Student', 'Student')
    )

    username= models.CharField(max_length=150, unique=True)
    email= models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role= models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.role})"

    def clean(self):
        if self.role:
            self.role = self.role.title()

    def save(self, *args, **kwargs):
        self.full_clean()  # calls clean() before saving
        super().save(*args, **kwargs)



