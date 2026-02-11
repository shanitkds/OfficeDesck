from rest_framework import serializers
from .models import Expense,SalaryStrucher
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
    class Meta:
        model=Expense
        fields=['id','user_name','amount','description','status','accountant_remark','created_at']
        
class SalaryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=SalaryStrucher
        fields = [
            'user',
            'basic_salary',
            'hra',
            'allowance',
            'deduction'
        ]