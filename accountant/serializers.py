from rest_framework import serializers
from .models import Expense,SalaryStrucher,Payment
from attendance.services import get_organisation

class ExplanseClimeRequestSerialicer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields=['amount','bill_file','description']
    
    def create(self, validated_data):
        user=self.context.get('user')
        
        expe=Expense.objects.create(
            user=user,
            organization=get_organisation(user),
            amount=validated_data['amount'],
            bill_file=validated_data.get('bill_file'),
            description=validated_data.get('description')
        )
        
        return expe
    
class ExpenseRejectAsseptSerializer(serializers.ModelSerializer):
    accountant_remark = serializers.CharField(required=False,allow_blank=True,allow_null=True)
    class Meta:
        model=Expense
        fields = ['status', 'accountant_remark']
            
        
class ExpenceViewSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user.name', read_only=True)
    user_employee_id=serializers.CharField(source='user.employee_id', read_only=True)
    class Meta:
        model=Expense
        fields=['id','user_name','user_employee_id','amount','description','status','accountant_remark','created_at']
        
class SalaryVieweSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user.name", read_only=True)
    user_employee_id = serializers.CharField(source="user.employee_id", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_mobile = serializers.CharField(source="user.phone", read_only=True)

    class Meta:
        model = SalaryStrucher
        fields = [
            'user',
            'user_name',
            'user_employee_id',
            'user_email',
            'user_mobile',
            'basic_salary',
            'hra',
            'allowance',
            'deduction'
        ]
        
class PaimentTableSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user.name", read_only=True)
    user_employee_id = serializers.CharField(source="user.employee_id", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_mobile = serializers.CharField(source="user.phone", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "user_name",
            "user_employee_id",
            "user_email",
            "user_mobile",
            "month",
            "salary_amount",
            "expense_amount",
            "total_amount",
            "status",
        ]
