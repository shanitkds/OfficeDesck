from django.db import models
from teamlead.models import TeamLead
from employee.models import Employee

class TaskAssignment(models.Model):

    STATUS_CHOICES = [
        ("ASSIGNED", "Assigned"),
        ("SUBMITTED", "Submitted"),
        ("RESUBMITTED","Resubmitted"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]


    title=models.CharField(max_length=50)
    description=models.TextField(null=True,blank=True)
    team_lead=models.ForeignKey(TeamLead,on_delete=models.CASCADE)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    team_lead_file=models.FileField(upload_to="task_files/team_lead/",null=True,blank=True)
    employee_file=models.FileField(upload_to="task_files/employee/",null=True,blank=True)
    employee_replay_note=models.TextField(null=True,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="ASSIGNED")
    created_at = models.DateTimeField(auto_now_add=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    last_submission_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} -{self.employee.user.employee_id} assine to {self.employee.user.name}"