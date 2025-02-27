from django.urls import path
from .views import CoustomTokenObtainPairView,CoustomTokenRefreshView,RegisterView,VerifyOTPView,AdminOnlyView,UserOnlyView,LogoutView
urlpatterns = [

    path('token/', CoustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CoustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/',RegisterView.as_view(),name="register"),
    path('otp-verification/',VerifyOTPView.as_view(),name="verifyotp"),
    path('adminView/',AdminOnlyView.as_view(),name="adminonlyview"),
    path('userView/',UserOnlyView.as_view(),name="useronlyview"),
    path('logout/',LogoutView.as_view(),name="logout"),

]