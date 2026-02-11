from django.utils.timezone import now
from services import auto_absent_mark as mark_absent
from attendance.models import AttendanceLog


def run_auto_absent(): #use in this crone
    if now().hour >= 11:
        mark_absent()