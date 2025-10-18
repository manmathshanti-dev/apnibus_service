from django.urls import path
from . import views

urlpatterns = [
    path('send-otp', views.SendOtpUserView.as_view(), name='user-otp-send'),
    path('verify-otp', views.VerifyOtpUserView.as_view(), name='user-otp-verify'),
]
