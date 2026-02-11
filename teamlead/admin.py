from django.contrib import admin
from .models import TeamLead,TeamLeadReview

# Register your models here.
class View_TeamLead(admin.ModelAdmin):
    list_display=('id',)

admin.site.register(TeamLead,View_TeamLead)
admin.site.register(TeamLeadReview)
