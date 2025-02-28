from rest_framework import serializers
from loan.models import Loan
from user.models import CustomUser
from loan.serializers import LoanSerializer

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']

class AllLoanListSerializer(serializers.ModelSerializer):
    monthly_installment = serializers.FloatField(read_only=True)
    total_interest = serializers.FloatField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)
    
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'amount', 'tenure', 'interest_rate', 'monthly_installment', 
                  'total_interest', 'total_amount','instalment']
        read_only_fields = ['loan_id', 'monthly_installment', 'total_interest', 
                            'total_amount']
        
        
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        details = instance.calculate_loan_details()
        return {
            "status": "success",
            "data": {
                "loan_id": data['loan_id'],
                "amount": float(data['amount']),
                "tenure": data['tenure'],
                "interest_rate": f"{data['interest_rate']}% yearly",
                "instalment paid":data['instalment'],
                "monthly_installment": details['monthly_installment'],
                "total_interest": details['total_interest'],
                "total_amount": details['total_amount']
                
                 
            }
        }
    
class UserLoanSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(many=True, read_only=True, source='loans') 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'loan']


class DeleteLoanSerializer(serializers.Serializer):
    loan_id = serializers.CharField(max_length=10)

    def validate_loan_id(self, value):
        try:
            Loan.objects.get(loan_id=value) 
        except Loan.DoesNotExist:
            raise serializers.ValidationError("Loan with this ID does not exist.")
        return value