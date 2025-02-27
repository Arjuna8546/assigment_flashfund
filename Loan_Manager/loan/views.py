from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoanSerializer,LoanListSerializer,LoanForeclosureSerializer
from .models import Loan


class LoanView(APIView):
    def post(self, request):
        serializer = LoanSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"status": "error", "errors": serializer.errors}, status=400)
    
    def get(self,request, loan_id=None):
        if loan_id:
            try:
                loan = Loan.objects.get(loan_id=loan_id,borrower=request.user)
                serializer = LoanListSerializer(loan)
                return Response(serializer.data)
            except Loan.DoesNotExist:
                return Response({"status": "error", "detail": "Loan not found"}, status=404)
        else:
            data = Loan.objects.filter(borrower=request.user)
            serializer = LoanSerializer(data, many=True)
            return Response(serializer.data)
    
class LoanForeclosureView(APIView):
    def post(self, request, loan_id):
        data = {"loan_id": loan_id}
        serializer = LoanForeclosureSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            try:
                response_data = serializer.to_representation(serializer.instance)
                return Response(response_data, status=200)
            except ValueError as e:
                return Response({"status": "error", "detail": str(e)}, status=400)
        return Response({"status": "error", "errors": serializer.errors}, status=400)
