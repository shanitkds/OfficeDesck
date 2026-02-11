from django.db import models
from account.models import User
from organizations.models import Oganisation
from teamlead.models import TeamLead

class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    organization=models.ForeignKey(Oganisation,on_delete=models.CASCADE,null=True,blank=True)
    team_lead=models.ForeignKey(TeamLead,on_delete=models.SET_NULL,null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    desigination=models.CharField(max_length=100,null=True,blank=True)
    face_encode = models.BinaryField(null=True, blank=True)
    photo=models.ImageField(upload_to='employ_photos/',null=True,blank=True)
    id_proof=models.FileField(upload_to='employid_proofs/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    
