# Create your views here.
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.convertors.user_serializer import UserSerializer


class MeView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.auth.user)
        return Response({"message": "Token valid", "user": user_data.data})
