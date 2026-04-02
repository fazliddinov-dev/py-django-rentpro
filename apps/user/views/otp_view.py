from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import SendOTPSerializer, VerifyOTPSerializer
from ..services.otp_service import OTPService
from ..services.token_service import TokenService


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        OTPService.send_otp(email=email)

        return Response(
            {"message": "OTP sent"},
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            user, created = OTPService.verify_otp(email, code)  # ← unpack tuple
        except PermissionError:
            return Response(
                {"error": "Too many attempts. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        tokens = TokenService.issue_tokens(user)

        return Response(
            {
                **tokens,
                "user": {"email": user.email},
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
