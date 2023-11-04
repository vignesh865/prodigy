from http import HTTPStatus

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils.auth_utils import AuthUtils
from integration.domain_models.source_type import SourceTypeValue
from integration.service.google_integration_service import GoogleIntegrationService


class LoadExternalFolder(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        source_type = request.GET.get('source_type')
        search_term = request.GET.get('search_term')
        tenant_id = AuthUtils.get_tenant(request).id

        if source_type == SourceTypeValue.GOOGLE_DRIVE.name:
            folders = GoogleIntegrationService.load_folders(tenant_id, SourceTypeValue.GOOGLE_DRIVE.name, search_term)
            return Response({"code": HTTPStatus.OK, "message": folders})

        return Response({"code": HTTPStatus.BAD_REQUEST,
                         "message": f"Not supported source - {source_type}"})
