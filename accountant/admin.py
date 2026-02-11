from django.contrib import admin
from .models import Accountent,Expense,Payment,SalaryStrucher
# Register your models here.
admin.site.register(Accountent)
admin.site.register(Expense)
admin.site.register(Payment)
admin.site.register(SalaryStrucher)
