from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExplanseClimeRequestSerialicer,ExpenseRejectAsseptSerializer,ExpenceViewSerializer,SalaryVieweSerializer,PaimentTableSerializer
from .models import Expense,SalaryStrucher,Payment
from attendance.services import get_organisation
from .services import add_expense_to_payment
from django.shortcuts import get_object_or_404
from account.models import User

# Create your views here.

class ExpemseClimeRequestAPIView(APIView):
    def post(self,request):
        user=request.user
        
        if user.user_type=='SUPER_ADMIN':
            return Response({"error":"You have no access"},status=status.HTTP_403_FORBIDDEN)
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
        type=request.GET.get('type')
        
        if user.user_type in ['ACCOUNTANT','ORG_ADMIN']:
            if type=="my":
                expenses=Expense.objects.filter(organization=org,user=user).order_by('-created_at')
            else:
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
        login_user = request.user

        if login_user.user_type not in ["ACCOUNTANT", "ORG_ADMIN"]:
            return Response(
                {"detail": "Only accountant or admin can add/update salary"},
                status=status.HTTP_403_FORBIDDEN
            )

        org = get_organisation(login_user)

        emp_id = request.data.get("employee_id")
        basic = request.data.get("basic_salary")
        hra = request.data.get("hra")
        allowance = request.data.get("allowance")
        deduction = request.data.get("deduction")

        if not emp_id:
            return Response({"detail": "Employee ID required"}, status=400)

        try:
            target_user = User.objects.get(employee_id=emp_id)
        except User.DoesNotExist:
            return Response({"detail": "Employee not found"}, status=404)


        basic = basic or 0
        hra = hra or 0
        allowance = allowance or 0
        deduction = deduction or 0

        salary, created = SalaryStrucher.objects.update_or_create(
            user=target_user,
            organization=org,
            defaults={
                "basic_salary": basic,
                "hra": hra,
                "allowance": allowance,
                "deduction": deduction,
            }
        )

        msg = "Salary created" if created else "Salary updated"
        return Response({"message": msg}, status=200)


    
class ViewSalary(APIView):
    def get(self,request):
        user=request.user
        org=get_organisation(user)
        
        if user.user_type not in ['ACCOUNTANT','ORG_ADMIN']:
            return Response( {"detail": "You do not have permission to view this salary."},status=status.HTTP_403_FORBIDDEN)
        
        salary=SalaryStrucher.objects.filter(organization=org)
        print(salary)
        serializer=SalaryVieweSerializer(salary,many=True)
        return Response(serializer.data)


class PaymentSettings(APIView):

    def get(self, request):
        user = request.user
        org = get_organisation(user)

        month = request.GET.get("month")
        salary_type = request.GET.get("salary")   # my / all

        payments = Payment.objects.filter(organization=org)

        if month:
            year, mon = month.split("-")
            payments = payments.filter(
                month__year=year,
                month__month=mon
            )

        if user.user_type in ["ACCOUNTANT", "ORG_ADMIN"]:

            if salary_type == "my":
                payments = payments.filter(user=user)

        else:
            payments = payments.filter(user=user)

        serializer = PaimentTableSerializer(payments, many=True)
        return Response(serializer.data)
        
    # def post(self,request):
        


    def patch(self, request):
        user = request.user
        org = get_organisation(user)

        payment_id = request.data.get("id")
        new_status = request.data.get("status", "PAID")
        month = request.data.get("month")
        year = request.data.get("year")

        if payment_id:
            payment = get_object_or_404(Payment, organization=org, id=payment_id)
            payment.status = new_status
            payment.save()
            return Response({"message": "Single payment updated"}, status=status.HTTP_200_OK)

        if month and year:
            try:
                month = int(month)
                year = int(year)
            except ValueError:
                return Response({"error": "Invalid month/year"}, status=400)

            updated = Payment.objects.filter(
                organization=org,
                created_at__month=month,
                created_at__year=year
            ).update(status=new_status)

            return Response(
                {"message": f"{updated} payments updated for {month}/{year}"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Provide id OR month and year"},
            status=status.HTTP_400_BAD_REQUEST
        )