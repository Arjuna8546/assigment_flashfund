from rest_framework.response import Response
from rest_framework.views import APIView
from user.permissions import IsAdmin
from loan.models import Loan
from user.models import CustomUser
from .serializers import AllLoanListSerializer,UserLoanSerializer,DeleteLoanSerializer
from rest_framework import status


class AllLoanView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        try:
            loans = Loan.objects.all().select_related('borrower')
            if not loans.exists():
                return Response({
                    "status": "success",
                    "message": "No loans found in the system.",
                    "data": []
                }, status=status.HTTP_200_OK)

            serializer = AllLoanListSerializer(loans, many=True)
            return Response({
                "status": "success",
                "message": "All loans retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred while retrieving loans.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class AllUserLoanView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        try:
            users = CustomUser.objects.all().prefetch_related('loans')
            if not users.exists():
                return Response({
                    "status": "success",
                    "message": "No users found in the system.",
                    "data": {
                        "users": []
                    }
                }, status=status.HTTP_200_OK)

            serializer = UserLoanSerializer(users, many=True)
            return Response({
                "status": "success",
                "message": "All users and their loans retrieved successfully.",
                "data": {
                    "users": serializer.data
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred while retrieving users and loans.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
        
            
