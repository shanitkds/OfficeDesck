from django.contrib import admin
from .models import Attendance,AttendanceRequest

# Register your models here.
admin.site.register(Attendance)
admin.site.register(AttendanceRequest)