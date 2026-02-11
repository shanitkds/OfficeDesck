from django.contrib import admin
from .models import SecureFile,FileShare

# Register your models here.
admin.site.register(SecureFile)
admin.site.register(FileShare)
