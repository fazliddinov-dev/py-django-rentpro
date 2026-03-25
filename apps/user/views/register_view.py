from ..services import register_service, token_service
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import RegisterSerializer,UserListSerializer
from rest_framework import status
from ..models import User

class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)


        user = register_service.register_user(serializer.validated_data)

        token = token_service.TokenService.issue_tokens(user)

        return Response({'token': str(token)}, status=status.HTTP_201_CREATED)

class ListUser(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

