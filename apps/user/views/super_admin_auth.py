from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.services.super_admin_login import SuperAdminLoginService

from ..serializers import LoginSerializer


class SuperAdminLoginView(APIView):
    """
    Super admin login endpoint using credentials from .env and SimpleJWT
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        use_case = SuperAdminLoginService()
        result = use_case.execute(username, password)
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
