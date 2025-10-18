from rest_framework import serializers

class SendOtpRequestSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)

class VerifyOtpRequestSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    otp = serializers.IntegerField()

class OtpResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    mobile = serializers.CharField()
    is_verified = serializers.BooleanField()
