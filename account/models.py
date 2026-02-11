from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        extra_fields.setdefault('is_active', True)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'SUPER_ADMIN')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    
    USER_TYPE_CHOICES = [
        ('SUPER_ADMIN', 'Super Admin'),
        ('ORG_ADMIN', 'Organization Admin'),
        ('TEAM_LEAD', 'Team Lead'),
        ('EMPLOYEE', 'Employee'),
        ('HR', 'HR'),
        ('ACCOUNTANT', 'Accountant'),
    ]
    
    ATTENDANCE_MODE = (
    ('FACE_ONLY', 'Face Only'),
    ('FACE_LOCATION', 'Face + Location'),
)
    
    name=models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=50, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    individual_attendance_mode = models.CharField(max_length=20,choices=ATTENDANCE_MODE,null=True,blank=True)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['employee_id']
    
    def __str__(self):
        return f"{self.email}-{self.id}"
    
    
    #  Attendance eligibility
    def is_attendance_required(self):
        return self.user_type in [
            'EMPLOYEE',
            'TEAM_LEAD',
            'ACCOUNTANT',
            'HR'
        ]

    # # ✅ Effective attendance mode
    # def get_attendance_mode(self):
    #     if not self.is_attendance_required():
    #         return None
    #     if self.individual_attendance_mode:
    #         return self.individual_attendance_mode
    #     return self.organization.attendance_mode
    
    