from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.services.super_admin_login import SuperAdminLoginService

from ..serializers import LoginSerializer


class SuperAdminLoginView(APIView):
    """
    Super admin login endpoint using credentials from .env and JWT
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        service = SuperAdminLoginService()
        result = service.execute(username=username, password=password)

        if not result:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(result, status=status.HTTP_200_OK)
