from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils.auth_utils import AuthUtils
from integration.domain_models.source_type import SourceTypeValue
from integration.service.source_credential_service import SourceCredentialService


class SourceIntegrateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant_id = AuthUtils.get_tenant(request).id
        sources = SourceCredentialService.get_all_integrated_sources(tenant_id)
        return Response({"sources": sources})

    def post(self, request):

        source_type = request.GET.get('source_type')

        request.session["redirect_data"] = SourceIntegrateView.get_redirection_data(request)

        tenant_id = AuthUtils.get_tenant(request).id
        is_credentials_present = SourceCredentialService.is_credentials_present(tenant_id, source_type)

        if is_credentials_present:
            return Response({"code": HTTPStatus.OK,
                             "message": f"Already connected to {source_type}"})

        if source_type == SourceTypeValue.GOOGLE_DRIVE.name:
            return redirect(reverse('google-drive') + f"?action=authorize")

        return Response({"code": HTTPStatus.BAD_REQUEST,
                         "message": f"Not supported source - {source_type}"})

    @staticmethod
    def get_redirection_data(request):
        user = AuthUtils.get_user(request)
        tenant = AuthUtils.get_tenant(request)
        return {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "login_hint": user.email
        }
