# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import AppUser


class LoginView(APIView):
    def post(self, request):
        user = get_object_or_404(AppUser, username=request.data['username'],
                                 tenant=request.data['tenant'])
        if not user.check_password(request.data['password']):
            return Response("missing user", status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': user.username, "is_new_token": created})
