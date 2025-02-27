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
    instalment = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.loan_id:
            last_loan = Loan.objects.order_by('-id').first()
            new_id  = int(last_loan.loan_id[4:])+1 if last_loan else 1
            self.loan_id = f"LOAN{new_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.loan_id} - {self.borrower.username}"
    
    def calculate_loan_details(self):
        principal = float(self.amount) 
        annual_rate = float(self.interest_rate) / 100  
        monthly_rate = annual_rate / 12  
        months = int(self.tenure)  

        if monthly_rate > 0:
            factor = (1 + monthly_rate) ** months  
            emi = (principal * monthly_rate * factor) / (factor - 1)  
        else:
            emi = principal / months

        total_amount = emi * months 
        total_interest = total_amount - principal

        return {
            "monthly_installment": round(emi, 2),  
            "total_amount": round(total_amount, 2),  
            "total_interest": round(total_interest, 2)  
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
    
    def get_loan_status(self):
        details = self.calculate_loan_details()
        emi = details["monthly_installment"]
        total_amount = details["total_amount"]

        installments_paid = min(self.instalment, self.tenure)  

        amount_paid = emi * installments_paid

        remaining_amount = total_amount - amount_paid

        schedule = self.generate_payment_schedule()
        if installments_paid < self.tenure:
            next_due_date = schedule[installments_paid]["due_date"]
        else:
            next_due_date = None 

        return {
            "amount_paid": round(amount_paid, 2),
            "remaining_amount": round(remaining_amount, 2),
            "next_due_date": next_due_date
        }
    
    def foreclose(self):
        if self.status in ['repaid']:
            raise ValueError("Loan is already settled.")

        status = self.get_loan_status()
        remaining_amount = status['remaining_amount']

        foreclosure_discount = round(remaining_amount * 0.05, 2)
        final_settlement_amount = round(remaining_amount - foreclosure_discount, 2)
        amount_paid = self.amount

        self.status = 'repaid'
        self.instalment = self.tenure  
        self.save()

        return {
            "loan_id": self.loan_id,
            "amount_paid": amount_paid,
            "foreclosure_discount": foreclosure_discount,
            "final_settlement_amount": final_settlement_amount,
            "status": self.status.upper()
        }