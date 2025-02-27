from user.models import CustomUser
from django.db import models
from dateutil.relativedelta import relativedelta

class Loan(models.Model):
    STATUS_CHOICES=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('repaid', 'Repaid'),
        ('defaulted', 'Defaulted'),
    )

    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='loans')
    loan_id = models.CharField(max_length=20, unique=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tenure = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if not self.loan_id:
            last_loan = Loan.objects.order_by('-id').first()
            new_id  = int(last_loan.loan_id[4:])+1 if last_loan else 1
            self.loan_id = f"LOAN{new_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.loan_id} - {self.borrower.username}"
    
    def calculate_loan_details(self):
        principal = float(self.amount)  # 10000
        annual_rate = float(self.interest_rate) / 100  # 0.1
        monthly_rate = annual_rate / 12  # 0.008333...
        months = int(self.tenure)  # 12

        if monthly_rate > 0:
            factor = (1 + monthly_rate) ** months  # (1 + 0.008333)^12 ≈ 1.104713
            emi = (principal * monthly_rate * factor) / (factor - 1)  # Unrounded EMI
        else:
            emi = principal / months

        total_amount = emi * months  # Use unrounded EMI first
        total_interest = total_amount - principal

        return {
            "monthly_installment": round(emi, 2),  # Round EMI for display
            "total_amount": round(total_amount, 2),  # Round after multiplication
            "total_interest": round(total_interest, 2)  # Round after subtraction
        }

    def generate_payment_schedule(self):

        details = self.calculate_loan_details()
        schedule = []
        start_date = self.created_date.date()

        for i in range(1,self.tenure + 1):
            due_date = start_date + relativedelta(months=i)
            schedule.append({
                "installment_no": i,
                "due_date": due_date.strftime("%Y-%m-%d"),
                "amount": details["monthly_installment"]
            })
        return schedule