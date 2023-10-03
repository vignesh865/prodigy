# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import AppUser
from authentication.serializers.UserSerializer import UserSerializer


class SignupView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        user = AppUser.objects.get(username=serializer.data['username'],
                                   tenant=serializer.data['tenant'])

        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
