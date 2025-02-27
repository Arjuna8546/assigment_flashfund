from django.urls import path
from .views import AddLoanView

urlpatterns = [
    path('',AddLoanView.as_view(),name="addLoan"),
]
