from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User
from ..serializers import RegisterSerializer, UserListSerializer
from ..services import register_service, token_service
from ..services.otp_service import OTPService


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        # Check email not already registered
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                {"email": "An account with this email already exists."}
            )

        OTPService.send_otp(
            email=email,
            registration_data=serializer.validated_data,  # ← pass it here
        )

        return Response(
            {"message": "OTP sent. Please verify your email to complete registration."},
            status=status.HTTP_200_OK,
        )


class ListUser(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
