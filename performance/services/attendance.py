from attendance.models import Attendance

def calculate_monthly_attendance(user,month,year):
    record=Attendance.objects.filter(
        user=user,
        date__month=month,
        date__year=year  
    )
    
    total_days=record.count()
    if total_days==0:
        return {
            "total_days": 0,
            "attendance_score": 0
        }
        
    points=0
    
    for r in record:
        if r.status=='FULL_DAY':
            points+=1
        elif r.status=='HALF_DAY':
            points+=0.5
            
    score=(points/total_days)*40
    
    return {
        "total_days": total_days,
        "attendance_score": round(score, 2)
    }