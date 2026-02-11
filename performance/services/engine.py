from .attendance import calculate_monthly_attendance
from .task import calculate_monthly_tasks
from .review import calculate_team_lead_review
from .ai import ai_performance_analysis
# from performance.models import PerformanceResult
import calendar


def generate_monthly_performance(employee, month, year):
    
    attendance = calculate_monthly_attendance(employee, month, year)
    task = calculate_monthly_tasks(employee, month, year)
    review = calculate_team_lead_review(employee, month, year)
    
    ai_result = ai_performance_analysis(
        attendance["attendance_score"],
        task["task_score"],
        review["review_score"]
    )
    
    return {
        "attendance": attendance,
        "task": task,
        "review": review,
        "final_score": ai_result["final_score"],
        "performance_level": ai_result["performance_level"]
    }
    

def month_name_to_number(month_name):
    if not month_name:
        return None

    month_name = month_name.strip().lower()

    for i in range(1, 13):
        if calendar.month_name[i].lower() == month_name:
            return i

    return None
    

# def save_performance(employee, organisation, team_lead, month, year, data):
#     PerformanceResult.objects.create(
#         organisation=organisation,
#         team_lead=team_lead,
#         employee=employee,
#         month=month,
#         year=year,
#         attendance_score=data['attendance']['attendance_score'],
#         task_score=data['task']['task_score'],
#         review_score=data['review']['review_score'],
#         final_score=data['final_score'],
#         performance_level=data['performance_level'],
        
#     )