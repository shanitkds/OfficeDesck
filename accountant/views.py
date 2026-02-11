from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExplanseClimeRequestSerialicer,ExpenseRejectAsseptSerializer,ExpenceViewSerializer,SalaryUpdateSerializer
from .models import Expense,SalaryStrucher
from attendance.services import get_organisation
from .services import add_expense_to_payment
from django.shortcuts import get_object_or_404

# Create your views here.

class ExpemseClimeRequestAPIView(APIView):
    def post(self,request):
        user=request.user
        
        if user.user_type=='SUPER_ADMIN':
            return Response({"You have no access"},status=status.HTTP_403_FORBIDDEN)
        serializer=ExplanseClimeRequestSerialicer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({
                    "message": "Expense submitted successfully",
                    "data": serializer.data
                },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request): #get expence as list
        user=request.user
        org=get_organisation(user)
        
        if user.user_type=='ACCOUNTANT':
            expenses=Expense.objects.filter(organization=org).order_by('-created_at')
        else:
            expenses=Expense.objects.filter(
                user=user,
                organization=org
            ).order_by('-created_at')
        serializer=ExpenceViewSerializer(expenses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    
class ExpenceApprovelAPIView(APIView):
    def patch(self,request,id):
        user=request.user
        
        if user.user_type !='ACCOUNTANT':
            return Response({"details":"You do not have permission to perform this action."},status=status.HTTP_403_FORBIDDEN)
        
        try:
            expense =Expense.objects.get(
                id=id,
                organization=get_organisation(user),
                status='PENDING'
            )
        except Expense.DoesNotExist:
            return Response(
                {"detail": "Expense not found or already processed."},
                status=status.HTTP_404_NOT_FOUND
            )
        if expense.status in ['APPROVED','REJECTED']:
            return Response({'Status must be APPROVED or REJECTED'})
        serializer=ExpenseRejectAsseptSerializer(expense,data=request.data,partial=True)
        if serializer.is_valid():
            expense =serializer.save()
            if expense.status=='APPROVED':
                add_expense_to_payment(expense)
            return Response({
                    "message": f"Expense {expense.status} successfully",
                    "data": serializer.data
                },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,id): #get uniq one
        user=request.user
        org=get_organisation(user)
        
        if user.user_type=='ACCOUNTANT':
            expenses=Expense.objects.filter(id=id,organization=org).order_by('-created_at')
        else:
            expenses=Expense.objects.filter(
                id=id,
                user=user,
                organization=org
            ).order_by('-created_at')
        serializer=ExpenceViewSerializer(expenses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class SalaryAddAPIView(APIView):
    def patch(self, request):
        user = request.user

        if user.user_type != 'ACCOUNTANT':
            return Response(
                {"detail": "Only accountant can add or update salary."},
                status=status.HTTP_403_FORBIDDEN
            )

        org = get_organisation(user)
        target_user = request.data.get('user')

        if not target_user:
            return Response(
                {"detail": "User is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        salary = SalaryStrucher.objects.filter(
            user=target_user,
            organization=org
        ).first()

        if salary:
            serializer = SalaryUpdateSerializer(
                salary,
                data=request.data,
                partial=True
            )
            action = "updated"

        else:
            serializer = SalaryUpdateSerializer(data=request.data)
            action = "created"

        if serializer.is_valid():
            serializer.save(organization=org)
            return Response(
                {"message": f"Salary {action} successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ViewUniqSalary(APIView):
    def get(self,request,id):
        user=request.user
        org=get_organisation(user)
        
        if user.user_type !='ACCOUNTANT':
            return Response( {"detail": "You do not have permission to view this salary."},status=status.HTTP_403_FORBIDDEN)
        
        salary=get_object_or_404(SalaryStrucher,user_id=id,organization=org)
        print(salary)
        serializer=SalaryUpdateSerializer(salary)
        return Response(serializer.data)
        
        
        