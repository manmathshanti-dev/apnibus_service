from common.models.base_model import BaseModel
from django.db import models

from user.models.user_model import User
from datetime import datetime, timedelta

def default_expiry():
    return datetime.now() + timedelta(minutes=5)



class UserOTP(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps",null=True,blank=True)
    otp = models.PositiveIntegerField(null=True,blank=True)
    is_verified = models.BooleanField(default=False,null=True,blank=True)
    expires_at = models.DateTimeField(default=default_expiry, null=True, blank=True)

    def __str__(self):
        return f"OTP for {self.user.mobile}: {self.otp} (Verified: {self.is_verified})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User OTP"
        verbose_name_plural = "User OTPs"