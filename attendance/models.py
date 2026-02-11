from django.db import models
from account.models import User

class Attendance(models.Model):
    
    ATTENDANCE_STATUS = (
    ('NOT_MARKED', 'Not Marked'),
    ('FULL_DAY', 'Full Day'),
    ('HALF_DAY', 'Half Day'),
    ('ABSENT', 'Absent'),
)
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=20,choices=ATTENDANCE_STATUS,default='NOT_MARKED')
    marked_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='marked_attendance')
    # face_verified = models.BooleanField(default=False)
    # location_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.name} - {self.date}"
    
    
class AttendanceRequest(models.Model):
    REQUEST_STATUS = (
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    attendance=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    reason=models.TextField()
    status=models.CharField(max_length=20,choices=REQUEST_STATUS,default='PENDING')
    reviewed_by =models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='attendance_reviews')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.status}-{self.id}"

class LeaveRequest(models.Model):
    REQUEST_STATUS = (
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    is_half_day=models.BooleanField(default=False)
    reason=models.TextField()
    status=models.CharField(max_length=20,choices=REQUEST_STATUS,default='PENDING')
    approved_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='leave_approvals')
    created_at = models.DateTimeField(auto_now_add=True)