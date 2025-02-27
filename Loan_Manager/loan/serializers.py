from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):

    monthly_installment = serializers.FloatField(read_only=True)
    total_interest = serializers.FloatField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)
    payment_schedule = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['loan_id', 'amount', 'tenure', 'interest_rate', 'monthly_installment', 
                  'total_interest', 'total_amount', 'payment_schedule']
        read_only_fields = ['loan_id', 'monthly_installment', 'total_interest', 'total_amount', 'payment_schedule']
    
    def validate(self, data):
        amount = data.get('amount')
        if amount is None or amount <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than 0."})
        if amount > 100000: 
            raise serializers.ValidationError({"amount": "Amount cannot exceed ₹100,000."})

    
        tenure = data.get('tenure')
        if tenure is None or tenure <= 3:
            raise serializers.ValidationError({"tenure": "Tenure must be greater than 3 months."})
        if tenure > 25:
            raise serializers.ValidationError({"tenure": "Tenure cannot exceed  24 months."})

        interest_rate = data.get('interest_rate')
        if interest_rate is None or interest_rate < 0:
            raise serializers.ValidationError({"interest_rate": "Interest rate cannot be negative."})
        if interest_rate > 100:
            raise serializers.ValidationError({"interest_rate": "Interest rate cannot exceed 100%."})

        return data

    def create(self, validated_data):
        validated_data['borrower'] = self.context['request'].user
        return Loan.objects.create(**validated_data)
    
    def get_payment_schedule(self, obj):
        return obj.generate_payment_schedule()
    
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
                "monthly_installment": details['monthly_installment'],
                "total_interest": details['total_interest'],
                "total_amount": details['total_amount'],
                "payment_schedule": data['payment_schedule']
            }
        }
