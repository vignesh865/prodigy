from http import HTTPStatus

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils.auth_utils import AuthUtils
from query_system.service.query_service import QueryService


class ChatController(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tenant = AuthUtils.get_tenant(request)

        query = request.data.get("query")

        assistant_response = QueryService.get_instance(tenant.id).answer_with_chain(query)["result"]
        return Response({"code": HTTPStatus.OK, "message": assistant_response})
