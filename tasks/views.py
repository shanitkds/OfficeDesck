from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TasckCreationSerializer,TaskViewSerializer,TaskSubmitSerializer,ApproveSerializer
from .models import TaskAssignment
from .models import Employee
from rest_framework import status
from django.shortcuts import get_object_or_404
from teamlead.models import TeamLead
from attendance.services import get_organisation



class GetPostTaskManageAPIView(APIView):
    def post(self,request):
        if request.user.user_type != "TEAM_LEAD":
            return Response({"error":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)
        
        serializer=TasckCreationSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Task created successfully"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        user=request.user
        org=get_organisation(user)
        
        if user.user_type in ['ORG_ADMIN','HR']:
            teamlead_id=request.query_params.get("em_id")
            employee=Employee(id=teamlead_id)
            tasks=TaskAssignment.objects.filter(employee=employee,organisation=org).order_by("-created_at")
        elif user.user_type=="EMPLOYEE":
            employee=user.employee
            tasks=TaskAssignment.objects.filter(employee=employee).order_by("-created_at")
        elif user.user_type=="TEAM_LEAD":
            employ_id=request.query_params.get("em_id")  #give this in frondent like this
            if not employ_id:
                return Response({"error":"employ_id is requerd"},status=status.HTTP_400_BAD_REQUEST)
            employee=Employee.objects.get(id=employ_id)
            team_lead=user.teamlead
            tasks=TaskAssignment.objects.filter(employee=employee,team_lead=team_lead).order_by("-created_at")
        else:
            return Response({"error":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)
        
        serializer=TaskViewSerializer(tasks,many=True)
        return Response(serializer.data)
    
class TaskGetApiView(APIView):  #get uniq task
    def get(self,request,id):
        user = request.user
        if user.user_type == "EMPLOYEE":
            task = get_object_or_404(TaskAssignment,id=id,employee=user.employee)
        elif user.user_type == "TEAM_LEAD":
            task = get_object_or_404(TaskAssignment,id=id,team_lead=user.teamlead)
        else:
            return Response({"error": "You are not authorized"},status=status.HTTP_403_FORBIDDEN)
        serializer = TaskViewSerializer(task)
        return Response(serializer.data)
class TaskSubmitView(APIView):
    def patch(self,request,id):
        if request.user.user_type !="EMPLOYEE":
            return Response({"error": "Only employees can submit tasks"},status=status.HTTP_403_FORBIDDEN)
        task=get_object_or_404(TaskAssignment,id=id,employee=request.user.employee)
        serialiser=TaskSubmitSerializer(task,data=request.data,partial=True)
        if serialiser.is_valid():
            serialiser.save()
            return Response({"updated"})
        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)
class ApproverDeletView(APIView):
    def patch(self,request,id):
        if request.user.user_type !="TEAM_LEAD":
            return Response({"error": "Only team lead can submit tasks"},status=status.HTTP_403_FORBIDDEN)
        task=get_object_or_404(TaskAssignment,id=id,team_lead=request.user.teamlead)
        serialiser=ApproveSerializer(task,data=request.data,partial=True)
        if serialiser.is_valid():
            serialiser.save()
            return Response({"set it"})
        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        if request.user.user_type !="TEAM_LEAD":
            return Response({"error": "Only team lead can delete tasks"},status=status.HTTP_403_FORBIDDEN)
        task=get_object_or_404(TaskAssignment,id=id,team_lead=request.user.teamlead)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response({"deleted"},status=status.HTTP_204_NO_CONTENT)
