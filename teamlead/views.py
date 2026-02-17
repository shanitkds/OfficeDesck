from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import TeamLead,TeamLeadReview
from employee.models import Employee
from .serializers import TeamMembersSerialiser,TeamLeadSerialise,TeamLeadReviewSerializer
from attendance.services import get_organisation

class TeamViewApi(APIView):
    def get_teamlead(self,user):
        if user.user_type == "TEAM_LEAD":
            return user.teamlead
        elif user.user_type=="EMPLOYEE":
            employ=user.employee
            return user.employee.team_lead
        return None
    
    def get(self,request):
        user=request.user
        
        if user.user_type in ["ORG_ADMIN","HR"]:
            org = get_organisation(user)

            teamleads = TeamLead.objects.filter(
                organization=org
            ).select_related("user")

            data = []

            for tl in teamleads:
                members = Employee.objects.filter(
                    team_lead=tl,
                    organization=org
                ).select_related("user")

                data.append({
                    "team_lead": TeamLeadSerialise(tl).data,
                    "team_members": TeamMembersSerialiser(
                        members, many=True
                    ).data
                })

            return Response(data)
        # ---------------------------------------------------------
        
        tem_lead=self.get_teamlead(user)
        
        if not tem_lead:
            if user.user_type == "TEAM_LEAD":
                return Response({"message":"You have no team assined"})
            elif user.user_type=="EMPLOYEE":
                return Response({"message":"You are not assigned to any team"})
            else:
                return Response({"error": "Permission denied"},status=status.HTTP_403_FORBIDDEN)
        
        team_head=TeamLeadSerialise(tem_lead)
        
        employ=Employee.objects.filter(team_lead=tem_lead,organization=tem_lead.organization)
        employ_data=TeamMembersSerialiser(employ,many=True)
        
        return Response({"team_lead":team_head.data,"team_members":employ_data.data})
        

class TeamLeadReviewAPIView(APIView):
    def post(self,request):
        user=request.user
        
        if user.user_type !='TEAM_LEAD':
            return Response({"detail": "You have no permission"},status=status.HTTP_403_FORBIDDEN)
        
        serializer=TeamLeadReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        employee=serializer.validated_data['employee']
        
        if employee.user_type != 'EMPLOYEE':
            return Response({"You can review only employees"},status=status.HTTP_400_BAD_REQUEST)
        
        user_org=get_organisation(user)
        employee_org=get_organisation(employee)
        
        if user_org !=employee_org:
            return Response({"Employee belongs to a different organisation"},status=status.HTTP_400_BAD_REQUEST)
        
        if employee.employee.team_lead!= user.teamlead:
            return Response({"This employee is not under your team"},status=status.HTTP_403_FORBIDDEN)
        
        review_date=serializer.validated_data["review_month"]
        
        exist=TeamLeadReview.objects.filter(
            team_lead=user,
            employee=employee,
            review_month__year=review_date.year,
            review_month__month=review_date.month
        ).exists()
        
        if exist:
            return Response({"Review already submitted for this employee this month"},status=status.HTTP_403_FORBIDDEN)
        
        TeamLeadReview.objects.create(
            organisation=user_org,
            team_lead=user,
            employee=employee,
            rating=serializer.validated_data["rating"],
            comment=serializer.validated_data.get("comment", ""),
            review_month=review_date
        )
        
        return Response({"detail": "Review submitted successfully"},status=status.HTTP_201_CREATED)