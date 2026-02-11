from django.db import models
from datetime import time

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
    creates_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name