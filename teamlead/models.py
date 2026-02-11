from django.db import models
from account.models import User
from organizations.models import Oganisation
from account.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class TeamLead(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    organization=models.ForeignKey(Oganisation,on_delete=models.CASCADE,null=True,blank=True)
    department = models.CharField(max_length=100)
    desigination=models.CharField(max_length=100,null=True,blank=True)
    face_encode = models.BinaryField(null=True, blank=True)
    photo=models.ImageField(upload_to='teamlead_photos/',null=True,blank=True)
    id_proof=models.FileField(upload_to='teadleadid_proofs/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    

# REVIEW

class TeamLeadReview(models.Model):
    organisation=models.ForeignKey(Oganisation,on_delete=models.CASCADE,related_name="teamlead_reviews")
    team_lead=models.ForeignKey(User,on_delete=models.CASCADE,related_name="reviews_given")
    employee=models.ForeignKey(User,on_delete=models.CASCADE,related_name="reviews_received")
    rating=models.PositiveSmallIntegerField(validators=[ MinValueValidator(1),MaxValueValidator(5)])
    comment=models.TextField(blank=True)
    
    review_month = models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together =("team_lead","employee","review_month")
        
    def __str__(self):
        return f"{self.employee} - {self.rating}"
    