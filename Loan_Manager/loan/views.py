from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoanSerializer,LoanListSerializer,LoanForeclosureSerializer
from .models import Loan
from rest_framework import status
from rest_framework import serializers

class LoanView(APIView):
    def post(self, request):
        serializer = LoanSerializer(data=request.data, context={'request': request})
        
        try:
            if serializer.is_valid(raise_exception=True):  
                loan = serializer.save()
                return Response({
                    "status": "success",
                    "message": f"Loan {loan.loan_id} created successfully.",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({
                "status": "error",
                "detail": "Invalid loan data.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred while creating the loan.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, loan_id=None):
        try:
            if loan_id:
                loan = Loan.objects.get(loan_id=loan_id, borrower=request.user)
                serializer = LoanListSerializer(loan)
                return Response({
                    "status": "success",
                    "message": f"Loan {loan_id} retrieved successfully.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                loans = Loan.objects.filter(borrower=request.user)
                if not loans.exists():
                    return Response({
                        "status": "success",
                        "message": "No loans found for this user.",
                        "data": []
                    }, status=status.HTTP_200_OK)
                serializer = LoanSerializer(loans, many=True)
                return Response({
                    "status": "success",
                    "message": "Loans retrieved successfully.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({
                "status": "error",
                "detail": "Loan not found or you don’t have permission."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred while retrieving loans.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class LoanForeclosureView(APIView):

    def post(self, request, loan_id):
        data = {"loan_id": loan_id}
        serializer = LoanForeclosureSerializer(data=data, context={'request': request})
        
        try:
            if serializer.is_valid(raise_exception=True):  
                response_data = serializer.to_representation(serializer.instance)
                return Response({
                    "status": "success",
                    "message": f"Loan {loan_id} foreclosed successfully.",
                    "data": response_data['data']  
                }, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({
                "status": "error",
                "detail": "Invalid foreclosure request.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                "status": "error",
                "detail": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred during foreclosure.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
