from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomTokenObtainPairSerializer,RegisterSerializer, VerifyOTPSerializer
from rest_framework import status
from .models import CustomUser
from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import serializers

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

            res = Response({
                "status": "success",
                "message": "Tokens generated successfully.",
            }, status=status.HTTP_200_OK)

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
        except serializers.ValidationError as e:
            return Response({
                "status": "error",
                "detail": "Invalid credentials or input data.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CoustomTokenRefreshView(TokenRefreshView):
    def post(self,request,*args,**kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")

            request.data["refresh"]= refresh_token

            response = super().post(request,*args,**kwargs)

            tokens = response.data
            access_token = tokens["access"]

            res = Response({
                "status": "success",
                "message": "Tokens refreshed successfully.",
            }, status=status.HTTP_200_OK)   

            res.set_cookie(
                key = "access_token",
                value = access_token,
                httponly = True,
                secure=True,
                samesite=None,
                path='/'
            )   
            return res     
        
        except serializers.ValidationError as e:
            return Response({
                "status": "error",
                "detail": "Invalid credentials or input data.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        try:
            if serializer.is_valid(raise_exception=True): 
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "User registered successfully. Check your email for OTP.",
                    "data": {
                        "email": serializer.validated_data.get('email')  
                    }
                }, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({
                "status": "error",
                "detail": "Invalid registration data.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred during registration.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        
        try:
            if serializer.is_valid(raise_exception=True):  # Raises ValidationError if invalid
                email = serializer.validated_data['email']
                otp = serializer.validated_data['otp']
                
                try:
                    user = CustomUser.objects.get(email=email)
                    if user.is_verified:
                        return Response({
                            "status": "error",
                            "detail": "Email is already verified."
                        }, status=status.HTTP_400_BAD_REQUEST)
                    if user.otp == otp:
                        user.is_active = True
                        user.is_verified = True
                        user.otp = None  # Clear OTP after verification
                        user.save()
                        return Response({
                            "status": "success",
                            "message": "Email verified successfully.",
                            "data": {
                                "email": email
                            }
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "status": "error",
                            "detail": "Invalid or expired OTP."
                        }, status=status.HTTP_400_BAD_REQUEST)
                except CustomUser.DoesNotExist:
                    return Response({
                        "status": "error",
                        "detail": "User not found."
                    }, status=status.HTTP_404_NOT_FOUND)
        except serializers.ValidationError as e:
            return Response({
                "status": "error",
                "detail": "Invalid input data.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred during OTP verification.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def get(self, request):
        try:
            return Response({
                    "status": "success",
                    "message": "Welcome, Admin!",
                    "data": {
                        "username": request.user.username,
                        "email": request.user.email,
                        "role": request.user.role
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                    "status": "error",
                    "detail": "An unexpected error occurred.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UserOnlyView(APIView):

    def get(self, request):
        try:
            return Response({
                    "status": "success",
                    "message": "Welcome, user",
                    "data": {
                        "username": request.user.username,
                        "email": request.user.email,
                        "role": request.user.role
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                    "status": "error",
                    "detail": "An unexpected error occurred.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class LogoutView(APIView):
    def post(self, request):
        try:

            if 'access_token' not in request.COOKIES:
                return Response({
                    "status": "success",
                    "message": "No active session found, but logout completed."
                }, status=status.HTTP_200_OK)

            response = Response({
                "status": "success",
                "message": "Logged out successfully.",
                "data": {
                    "email": request.user.email if request.user.is_authenticated else None
                }
            }, status=status.HTTP_200_OK)

            response.delete_cookie(
                key='access_token',
                path='/',
                samesite='None' 
            )

            if 'refresh_token' in request.COOKIES:
                response.delete_cookie(
                    key='refresh_token',
                    path='/',
                    samesite='None'
                )

            return response

        except Exception as e:
            return Response({
                "status": "error",
                "detail": "An unexpected error occurred during logout.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
