from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoanSerializer

class AddLoanView(APIView):
    def post(self, request):
        serializer = LoanSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"status": "error", "errors": serializer.errors}, status=400)