from django.db import models
from datetime import time
from account.models import User

class Oganisation(models.Model):
    ATTENDANCE_MODE = (
    ('FACE_ONLY', 'Face Only'),
    ('FACE_LOCATION', 'Face + Location'),
)
    name=models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=20)
    address=models.TextField()
    registration_doc=models.FileField(upload_to='org_documents/',null=True,blank=True)
    registration_number=models.CharField(max_length=100,null=True,blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    attendance_mode=models.CharField(max_length=20,choices=ATTENDANCE_MODE,default='FACE_LOCATION')
    full_day_last_time=models.TimeField(default=time(10,0))
    half_day_cutoff_time = models.TimeField(default=time(12, 0))
    is_active = models.BooleanField(default=True)
    creates_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class OrganizationRequest(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    ATTENDANCE_MODE = (
        ('FACE_ONLY', 'Face Only'),
        ('FACE_LOCATION', 'Face + Location'),
    )

    
    org_name = models.CharField(max_length=150)
    org_email = models.EmailField()
    org_phone = models.CharField(max_length=15, blank=True)
    org_address = models.TextField(blank=True)

    registration_doc = models.FileField(upload_to="org_docs/", null=True, blank=True)
    registration_number = models.CharField(max_length=100)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    attendance_mode = models.CharField(max_length=20, choices=ATTENDANCE_MODE)
    full_day_last_time = models.TimeField(null=True, blank=True)
    half_day_cutoff_time = models.TimeField(null=True, blank=True)

    
    admin_name = models.CharField(max_length=100)
    admin_email = models.EmailField()
    admin_phone = models.CharField(max_length=15, blank=True)

    admin_password = models.CharField(max_length=255)  # store HASHED password

    admin_photo = models.ImageField(upload_to="org_admin/photo/", null=True, blank=True)
    admin_id_proof = models.FileField(upload_to="org_admin/idproof/", null=True, blank=True)

    
    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="org_requests"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_org_requests"
    )

    rejection_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.org_name} - {self.status}"