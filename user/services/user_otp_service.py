import random
from datetime import datetime, timedelta

from common.service.base_service import BaseService
from common.utility.generate_otp_utility import generate_otp
from user.repositories.user_repo import UserRepository
from user.repositories.userotp_repo import UserOTPRepository

class OtpService(BaseService):
    def __init__(self):
        self.user_repo = UserRepository()
        self.otp_repo = UserOTPRepository()


    def send_otp(self, mobile: str):
        user = self.user_repo.get_first(filters=[("mobile", mobile)], error=False)
        
        if not user:
            user = self.user_repo.create(values={"mobile": mobile})

        otp_code = generate_otp()
        expires_at = datetime.now() + timedelta(minutes=5)

        self.otp_repo.create({
            "user": user,
            "otp": otp_code,
            "expires_at": expires_at
        })

        print(f"[DEBUG] OTP for {mobile}: {otp_code}")

        return self.ok({
            "message": "OTP sent successfully.",
            "mobile": mobile,
            "is_verified": user.is_verified
        })

    def verify_otp(self, mobile: str, otp: int):
        user = self.user_repo.get_first(filters=[("mobile", mobile)], error=False)
        if not user:
            return self.exception("User not found", 404)

        otp_obj = self.otp_repo.get_latest(
            filters=[
                ("user", user),
                ("is_verified", False)
            ],
            error=False
        )

        if not otp_obj:
            return self.exception("No valid OTP found. Request again.", 400)

        if otp_obj.expires_at < datetime.now():
            return self.exception("OTP expired. Please request a new one.", 400)

        if otp_obj.otp != otp:
            return self.exception("Invalid OTP", 400)

        self.otp_repo.update_where(query=[("id", otp_obj.id)], update=[("is_verified", True)])
        self.user_repo.UpdateWhere(query=[("id", user.id)], update=[("is_verified", True)])

        return self.ok({
            "message": "OTP verified successfully.",
            "mobile": mobile,
            "is_verified": True
        })
