from django.db import models
from account.models import User
from organizations.models import Oganisation

class Accountent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    organization=models.ForeignKey(Oganisation,on_delete=models.CASCADE,null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    desigination=models.CharField(max_length=100,null=True,blank=True)
    face_encode = models.BinaryField(null=True, blank=True)
    photo=models.ImageField(upload_to='employ_photos/',null=True,blank=True)
    id_proof=models.FileField(upload_to='employid_proofs/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    
   
class Expense(models.Model):
    STSATUS=[
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected')
        ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    organization=models.ForeignKey(Oganisation,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    bill_file=models.FileField(upload_to='expence_bills',null=True,blank=True)
    description=models.TextField(blank=True)
    status=models.CharField(choices=STSATUS,default='PENDING')
    accountant_remark= models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}"
    
class SalaryStrucher(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    organization =models.ForeignKey(Oganisation,on_delete=models.CASCADE)
    
    basic_salary=models.DecimalField(max_digits=10,decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}"
    
class Payment(models.Model):
    STATUS=[
            ('PENDING', 'Pending'),
            ('PAID', 'Paid')
        ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    organization =models.ForeignKey(Oganisation,on_delete=models.CASCADE)
    
    month=models.DateField()   
    
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
    status =models.CharField(
        choices=STATUS,max_length=10,default='PENDING'
    )
    
    paid_on = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class PaymentExpense(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE)