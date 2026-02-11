from django.db import models
from organizations.models import Oganisation
from account.models import User

class Organisation_admin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    organization=models.ForeignKey(Oganisation,on_delete=models.CASCADE,null=True,blank=True)
    photo=models.ImageField(upload_to='admin_photos/',null=True,blank=True)
    id_proof=models.FileField(upload_to='id_proofs/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    