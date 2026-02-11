from datetime import date
from .models import Attendance
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from account.models import User

def get_today_attentance(user):
    attentance,create=Attendance.objects.get_or_create(
        user=user,
        date=date.today()
    )
    return attentance

def get_organisation(user):
    if user.user_type =="EMPLOYEE":
        return user.employee.organization
    elif user.user_type=="TEAM_LEAD":
        return user.teamlead.organization
    elif user.user_type=="HR":
        return user.hr.organization
    elif user.user_type == "ACCOUNTANT":
        return user.accountent.organization
    elif user.user_type=="ORG_ADMIN":
        return user.organisation_admin.organization
    else:
        return None
    
            
    
def mark_attentance(user):
    if not user.is_attendance_required():
        raise PermissionDenied("Attendance not required for this user")
    attendance=get_today_attentance(user)
    
    if attendance.status in ['FULL_DAY', 'HALF_DAY']:
        return attendance
    
    now=timezone.localtime().time()
    
    org=get_organisation(user)
    if not org:
        raise PermissionDenied("Invalid user type")
    full_time=org.full_day_last_time
    half_time=org.half_day_cutoff_time
    
    if now > half_time:
        raise PermissionDenied("Attendance time is over")
    
    if now<=full_time:
        attendance.status='FULL_DAY'
    elif now<=half_time:
        attendance.status='HALF_DAY'
    else:
        attendance.status='ABSENT'
        
    attendance.marked_by=user
    attendance.save()
    
    return attendance

def prossess_attentance(user,face_verification,location_verfication):
    
    if not face_verification:
        raise PermissionDenied("Face verification failed")
    if user.individual_attendance_mode=='FACE_LOCATION' and not location_verfication:
        raise PermissionDenied("Location verification failed")
    
    attendance=mark_attentance(user)
    
    return attendance

def auto_absent_mark():
    today=date.today()
    now = timezone.localtime().time()
    
    users=User.objects.all()
    
    for user in users:
        if not user.is_attendance_required():
            continue
        
        org=get_organisation(user)
        if not org:
            continue
        
        # if now <= org.half_day_cutoff_time:
        #     continue
        attentence,create=Attendance.objects.get_or_create(
            user=user,
            date=today
        )
        
        if attentence.status in ['FULL_DAY', 'HALF_DAY']:
            continue
        attentence.status='ABSENT'
        attentence.marked_by=None
        attentence.save()
        
        
        
# -----------------------------------------------------------
# Attentanse Request


from django.utils import timezone
from rest_framework.exceptions import PermissionDenied


def handle_attendance_request_action(attendance_request, reviewer, action, day_type):
    request_user = attendance_request.user

    if request_user.user_type == 'HR' and reviewer.user_type != 'ORG_ADMIN':
        raise PermissionDenied("Only admin can approve HR requests")

    if request_user.user_type != 'HR' and reviewer.user_type not in ['ORG_ADMIN', 'HR']:
        raise PermissionDenied("You are not allowed to approve this request")

    if attendance_request.status != 'PENDING':
        raise PermissionDenied("This request is already processed")

    if action == 'APPROVE':
        attendance_request.status = 'APPROVED'

        attendance_request.attendance.status = day_type
        attendance_request.attendance.marked_by = reviewer
        attendance_request.attendance.save()

    elif action == 'REJECT':
        attendance_request.status = 'REJECTED'

    attendance_request.reviewed_by = reviewer
    attendance_request.reviewed_at = timezone.now()
    attendance_request.save()

    return attendance_request


# Manuale


def manual_attendance_upsert(editor, target_user, date, status):
    # Permission check
    if editor.user_type not in ['ORG_ADMIN', 'HR']:
        raise PermissionDenied("You are not allowed to modify attendance")

    # HR cannot edit own attendance
    if editor.user_type == 'HR' and editor == target_user:
        raise PermissionDenied("HR cannot modify their own attendance")

    # Create or update attendance
    attendance, created = Attendance.objects.get_or_create(
        user=target_user,
        date=date,
        defaults={
            'status': status,
            'marked_by': editor
        }
    )

    if not created:
        attendance.status = status
        attendance.marked_by = editor
        attendance.save()

    return attendance, created