from tasks.models import TaskAssignment

def calculate_task_score(task):
    if task.status !='APPROVED':
        return 0
    
    score=0
    
    if not task.submission_date or not task.last_submission_date:
        return 10
    
    if task.submission_date and task.last_submission_date:
        allowed_days = (task.last_submission_date - task.created_at).days
        taken_days = (task.submission_date - task.created_at).days

        if allowed_days > 0:
            if taken_days <= allowed_days * 0.5:
                score += 10
            elif taken_days <= allowed_days:
                score += 7
            else:
                score += 4
    
    return score
    

def calculate_monthly_tasks(employee, month, year):
    emplyeeeinstants=employee.employee
    tasks=TaskAssignment.objects.filter(
        employee=emplyeeeinstants,
        created_at__month=month,
        created_at__year=year
    )
    
    if not tasks.exists():
        return {
            "total_tasks": 0,
            "task_score": 0
        }
        
    total_score = 0
    approved_count = 0
    max_score = tasks.count() * 25
    
    for task in tasks:
        task_points=calculate_task_score(task)
        if task_points>0:
            approved_count += 1
        total_score+=task_points
        
    final_score =(total_score/max_score)*40
    
    return{
        "total_tasks": tasks.count(),
        "approved_tasks": approved_count,
        "task_score": round(final_score, 2)
    }
    