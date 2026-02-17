from performance.services.engine import month_name_to_number
from attendance.services import get_organisation
from performance.models import PerformanceResult



def get_performance_queryset(request, user):
    month_input = request.query_params.get("month")
    year = request.query_params.get("year")
    month = month_name_to_number(month_input) if month_input else None

    employee_id = request.query_params.get("employee_id")
    employee_name = request.query_params.get("employee_name")
    team_lead_id = request.query_params.get("team_lead_id")
    team_lead_name = request.query_params.get("team_lead_name")

    organisation = get_organisation(user)

    if user.user_type in ["ORG_ADMIN", "HR"]:
        queryset = PerformanceResult.objects.filter(organisation=organisation)
    elif user.user_type == "TEAM_LEAD":
        queryset = PerformanceResult.objects.filter(team_lead=user)
    elif user.user_type == "EMPLOYEE":
        queryset = PerformanceResult.objects.filter(employee=user)
    else:
        return PerformanceResult.objects.none()

    if month:
        queryset = queryset.filter(month=month)
    if year:
        queryset = queryset.filter(year=year)
    if employee_id:
        queryset = queryset.filter(employee__employee_id=employee_id)
    if employee_name:
        queryset = queryset.filter(employee__name__icontains=employee_name)
    if team_lead_id:
        queryset = queryset.filter(team_lead__employee_id=team_lead_id)
    if team_lead_name:
        queryset = queryset.filter(team_lead__name__icontains=team_lead_name)

    return queryset
