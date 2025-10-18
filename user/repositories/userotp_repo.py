

from common.repository.base_repository import BaseRepository
from user.models.otp_model import UserOTP


class UserOTPRepository(BaseRepository):
    def __init__(self):
        self.model = UserOTP
