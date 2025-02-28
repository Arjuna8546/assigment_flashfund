from rest_framework.response import Response
from rest_framework.views import APIView
from user.permissions import IsAdmin
from loan.models import Loan
from user.models import CustomUser
from .serializers import AllLoanListSerializer,UserLoanSerializer,DeleteLoanSerializer
from rest_framework import status


class AllLoanView(APIView):
    permission_classes = [IsAdmin]
    def get(self,request):
        loan = Loan.objects.all()
        serializer = AllLoanListSerializer(loan,many=True)
        return Response(serializer.data)
    
class AllUserLoanView(APIView):
    permission_classes = [IsAdmin]
    def get(self,request):
        users = CustomUser.objects.all().prefetch_related('loans')  
        serializer = UserLoanSerializer(users, many=True)
        
        return Response({
            "status": "success",
            "data": {
                "users": serializer.data
            }
        })
    
class DeleteLoan(APIView):
    permission_classes=[IsAdmin]

    def delete(self, request):
        serializer = DeleteLoanSerializer(data=request.data)
        if serializer.is_valid():
            try:
                loan_id = serializer.validated_data['loan_id']
                loan = Loan.objects.get(loan_id=loan_id)
                loan.delete()
                return Response({
                    "status": "success",
                    "message": f"Loan {loan_id} deleted successfully."
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "status": "error",
                    "detail": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)       
        
            
