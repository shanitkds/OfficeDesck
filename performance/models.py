from django.db import models
from account.models import User
from organizations.models import Oganisation

# Create your models here.

class PerformanceResult(models.Model):
    PERFORMANCE_LEVEL = (
        ("EXCELLENT", "Excellent"),
        ("GOOD", "Good"),
        ("AVERAGE", "Average"),
        ("POOR", "Poor"),
    )
    
    organisation = models.ForeignKey(Oganisation,on_delete=models.CASCADE,related_name="performance_results")
    team_lead =models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="team_performance")
    employee = models.ForeignKey(User,on_delete=models.CASCADE,related_name="performance_results")
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    attendance_score = models.FloatField()
    task_score = models.FloatField()
    review_score = models.FloatField()
    final_score = models.FloatField()
    performance_level = models.CharField(max_length=20,choices=PERFORMANCE_LEVEL)
    generated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("employee", "month", "year")
        
    def __str__(self):
        return f"{self.employee} | {self.month}/{self.year} | {self.performance_level}"
    