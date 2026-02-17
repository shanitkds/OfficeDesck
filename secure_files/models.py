from django.db import models
from account.models import User
from teamlead.models import TeamLead
from organizations.models import Oganisation


class SecureFile(models.Model):
    original_name=models.CharField(max_length=150)
    file_type=models.CharField(max_length=20)
    mime_type=models.CharField(max_length=100)
    
    encrypted_file=models.FileField(upload_to="secure_files/")
    encrypted_file_key =models.BinaryField(null=True,blank=True)
    
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    owner_role=models.CharField(max_length=30)
    
    team_lead =models.ForeignKey(TeamLead,null=True,blank=True,on_delete=models.SET_NULL)
    
    organization=models.ForeignKey(Oganisation,on_delete=models.CASCADE)
    
    allow_view=models.BooleanField(default=True)
    allow_download =models.BooleanField(default=True)
    allow_share =models.BooleanField(default=False)
    
    created_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}--{self.owner.name}"
    
class FileShare(models.Model):
    file=models.ForeignKey(SecureFile,on_delete=models.CASCADE)
    shared_with=models.ForeignKey(User,on_delete=models.CASCADE,related_name="files_shared_with_me",null=True,blank=True)
    message=models.CharField(null=True,blank=True)
    can_view=models.BooleanField(default=True)
    can_download = models.BooleanField(default=True)
    
    shared_by=models.ForeignKey(User,on_delete=models.CASCADE, related_name="files_shared_by_me")
    shared_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}"
    