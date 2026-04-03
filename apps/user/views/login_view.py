# views/login_view.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import LoginSerializer
from ..services.login_service import LoginService
from ..services.token_service import TokenService


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = LoginService.login(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        tokens = TokenService.issue_tokens(user)

        return Response(
            {
                **tokens,
                "user": {"email": user.email},
            },
            status=status.HTTP_200_OK,
        )
