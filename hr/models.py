from django.db import models
from account.models import User
from organizations.models import Oganisation

class HR(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,)
    organization=models.ForeignKey(Oganisation,on_delete=models.CASCADE,null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    desigination=models.CharField(max_length=100,null=True,blank=True)
    face_encode = models.BinaryField(null=True, blank=True)
    photo=models.ImageField(upload_to='hr_photos/',null=True,blank=True)
    id_proof=models.FileField(upload_to='hrid_proofs/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    



class EmployeeRequest(models.Model):

    ACTION_CHOICES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    name = models.CharField(max_length=200)
    employee_id=models.CharField(null=True,blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=200,null=True,blank=True)   

    user_type = models.CharField(max_length=50)   
    attendance_mode = models.CharField(max_length=50, blank=True, null=True)

    department = models.CharField(max_length=200, blank=True, null=True)
    designation = models.CharField(max_length=200, blank=True, null=True)
    
    phone = models.CharField(max_length=20, blank=True, null=True)

    photo = models.ImageField(upload_to="request/photo/", blank=True, null=True)
    id_proof = models.FileField(upload_to="request/idproof/", blank=True, null=True)

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
