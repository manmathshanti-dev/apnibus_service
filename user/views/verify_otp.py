from common.api.base_api_view import BaseAPIView
from user.serializers.otp_serializers import OtpResponseSerializer, VerifyOtpRequestSerializer
from user.services.user_otp_service import OtpService


class VerifyOtpUserView(BaseAPIView):
    def __init__(self, **kwargs):
        self.service = OtpService()
        super().__init__(**kwargs)

    def post(self, request):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return self.validation_failed(**serializer.errors)

        response = self.service.verify_otp(
            mobile=serializer.validated_data["mobile"],
            otp=serializer.validated_data["otp"]
        )

        if response["success"]:
            output = OtpResponseSerializer(data=response["response_data"])
            if output.is_valid():
                return self.success(output.data)

        return self.error_message(response["errors"], response["code"])
