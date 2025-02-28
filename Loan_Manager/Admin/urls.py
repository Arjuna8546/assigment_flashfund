from django.urls import path

from .views import AllLoanView,AllUserLoanView,DeleteLoan

urlpatterns = [
    path('loans/',AllLoanView.as_view(),name= "allLoan"),
    path('loans/users/',AllUserLoanView.as_view(),name= "all-user-Loan"),
    path('loans/delete/',DeleteLoan.as_view(),name ="delete-loan")
]
