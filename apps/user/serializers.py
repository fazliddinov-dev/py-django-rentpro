from rest_framework import serializers

from .models import EmailOTP, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "full_name", "phone_number"]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "phone_number",
            "role",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SendOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailOTP
        fields = ["email"]


class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailOTP
        fields = ["email", "code"]
