from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from attendance.services import get_organisation
from employee.models import Employee
from .models import PerformanceResult
from performance.services.engine import generate_monthly_performance,month_name_to_number
from .serializers import ViewPerformenceSerializer

# Create your views here.


class GenaratePerformenceAPIView(APIView):
    def post(self,request):
        user=request.user
        organisation=get_organisation(user)
        
        if user.user_type not in ['ORG_ADMIN','HR']:
            return Response({"error":"You are not authorized"},status=status.HTTP_403_FORBIDDEN)
        
        month_name=request.data.get('month')
        year=request.data.get('year')
        
        month=month_name_to_number(month_name)
        
        if not month or not year:
            return Response({"error":"month and year are required"},status=status.HTTP_400_BAD_REQUEST)
        employees=Employee.objects.filter(
            organization=organisation
        )
        
        create=0
        skipped=0
        
        for em in employees:
            employee=em.user
            teamlead=em.team_lead.user if em.team_lead else None
            
            exist=PerformanceResult.objects.filter(
                employee=employee,
                month=month,
                year=year
            ).exists()
            
            if exist:
                skipped+=1
                continue
            
            data=generate_monthly_performance(employee,month,year)
            
            PerformanceResult.objects.create(
                organisation=organisation,
                team_lead=teamlead,
                employee=employee,
                month=month,
                year=year,
                attendance_score=data['attendance']['attendance_score'],
                task_score=data['task']['task_score'],
                review_score=data['review']['review_score'],
                final_score=data['final_score'],
                performance_level=data['performance_level'],
        
            )
            
            create+=1
            
        return Response(
            {
                "message": "Organisation performance generated successfully",
                "organisation": organisation.name,
                "month": month,
                "year": year,
                "created_records": create,
                "skipped_existing": skipped,
                "total_employees": employees.count()
            },
            status=status.HTTP_201_CREATED
        )
        
class ViewPerformenceAPIView(APIView):
    def get(self,request):
        user=request.user
        
        month_input=request.query_params.get('month')
        year=request.query_params.get('year')
        
        month=month_name_to_number(month_input) if month_input else None
        
        employee_id = request.query_params.get("employee_id")
        employee_name = request.query_params.get("employee_name")

        team_lead_id = request.query_params.get("team_lead_id")
        team_lead_name = request.query_params.get("team_lead_name")
        
        
        organisation=get_organisation(user)
        
        if user.user_type in ['ORG_ADMIN','HR']:
            queryset=PerformanceResult.objects.filter(
                organisation=organisation
            )
        elif user.user_type=='TEAM_LEAD':
            queryset=PerformanceResult.objects.filter(
                team_lead=user
            )
            
        elif user.user_type=='EMPLOYEE':
            queryset=PerformanceResult.objects.filter(
                employee=user
            )
        else:
             return Response({"detail": "Unauthorized role"},
                status=status.HTTP_403_FORBIDDEN)
             
        if month:
            queryset=queryset.filter(month=month)
        if year:
            queryset=queryset.filter(year=year)
            
        if employee_id:
            queryset = queryset.filter(employee__employee_id=employee_id)

        if employee_name:
            queryset = queryset.filter(
                employee__name__icontains=employee_name
            )

        # 👨‍💼 Team lead filters
        if team_lead_id:
            queryset = queryset.filter(team_lead__employee_id=team_lead_id)

        if team_lead_name:
            queryset = queryset.filter(
                team_lead__name__icontains=team_lead_name
            )
            
        if not queryset:
            return Response({"error":"No data"},status=status.HTTP_400_BAD_REQUEST)
            
        serializer=ViewPerformenceSerializer(queryset,many=True)
        return Response(serializer.data)
        
        