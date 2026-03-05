from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers.user_serializers import LoginSerializer
from container.user_container import login_user_use_case
from core.user.application.dto.auth_dto import LoginInputDTO


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = LoginInputDTO(**serializer.validated_data)

        use_case = login_user_use_case()
        token = use_case.execute(dto)

        return Response({"access_token": token})
