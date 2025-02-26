from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomTokenObtainPairSerializer,RegisterSerializer, VerifyOTPSerializer
from rest_framework import status
from .models import CustomUser
from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class CoustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self,request,*args,**kwargs):
        try:
            response = super().post(request,*args,**kwargs)
            tokens = response.data

            access_token = tokens['access']
            refresh_token = tokens['refresh']

            res = Response()

            res.data = {"success":True}

            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite=None,
                path='/'
            )
            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite=None,
                path='/'
            )

            return res
        except:
            return Response({"success":False})
        

class CoustomTokenRefreshView(TokenRefreshView):
    def post(self,request,*args,**kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")

            request.data["refresh"]= refresh_token

            response = super().post(request,*args,**kwargs)

            tokens = response.data
            access_token = tokens["access"]

            res = Response() 

            res.data = {"refresh":True}    

            res.set_cookie(
                key = "access_token",
                value = access_token,
                httponly = True,
                secure=True,
                samesite=None,
                path='/'
            )   
            return res     
        
        except:
            return Response({"refresh":False})
        
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered,check your mail for OTP '}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = CustomUser.objects.get(email=email)
                if user.otp == otp and not user.is_verified:
                    user.is_active = True
                    user.is_verified = True
                    user.save()
                    return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({'message': 'Welcome, Admin!'})
    
class UserOnlyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': f'Hello, {request.user.role} {request.user.email}'})

