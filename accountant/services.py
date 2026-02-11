from django.utils.timezone import now
from .models import Payment,PaymentExpense,SalaryStrucher
from rest_framework.exceptions import PermissionDenied
from datetime import timedelta
from django.utils.timezone import now



def add_expense_to_payment(expense):
    today=now().date()
    current=today.replace(day=1)
    
    payment,create=Payment.objects.get_or_create(
        user=expense.user,
        organization=expense.organization,
        month=current,
    )
    
    if payment.status=='PAID':
        raise PermissionDenied("Payment for this month is already PAID. Cannot add expense.")
    
    if PaymentExpense.objects.filter(expense=expense).exists():
        return
    
    PaymentExpense.objects.create(
        payment=payment,
        expense=expense
    )
    
    payment.expense_amount+=expense.amount
    payment.total_amount+=expense.amount
    payment.save()
    

def salary_to_payment(user,organisation,month):
    payment,_=Payment.objects.get_or_create(
        user=user,organization=organisation,month=month
    )
    
    if payment.salary_amount>0:
        return
    
    if payment.status=='PAID':
        raise PermissionDenied("Payment for this month is already PAID."    )
    
    salary = SalaryStrucher.objects.filter(
    user=user,
    organization=organisation
).first()
    
    if not salary:
        return
    
    salary_amount=(
        salary.basic_salary+
        salary.hra+
        salary.allowance-
        salary.deduction
    )
    
    payment.salary_amount+=salary_amount
    payment.total_amount+=salary_amount
    payment.save()
    
def salary_payment_automation():
    
    today = now().date()

    first_day_this_month = today.replace(day=1)
    last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)
    
    salarys=SalaryStrucher.objects.all()
    
    for salary in salarys:
        salary_to_payment(
            salary.user,
            salary.organization,
            last_month
        )