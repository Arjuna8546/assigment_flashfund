from django.urls import path
from .views import LoanView,LoanForeclosureView

urlpatterns = [
    path('',LoanView.as_view(),name="addLoan"),
    path('<str:loan_id>/', LoanView.as_view(), name='loan-detail'),
    path('<str:loan_id>/foreclose/',LoanForeclosureView.as_view(),name="loanForeclose")
]
