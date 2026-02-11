from django.contrib import admin
from .models import Employee

# Register your models here.

class View_Employ(admin.ModelAdmin):
    list_display = ('id', 'face_encode_preview')

    def face_encode_preview(self, obj):
        if obj.face_encode:
            return obj.face_encode[:20]  # show first 20 bytes
        return "No Data"

    face_encode_preview.short_description = "Face Encode Preview"
admin.site.register(Employee,View_Employ)
