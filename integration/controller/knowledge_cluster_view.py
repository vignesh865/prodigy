from http import HTTPStatus

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils.auth_utils import AuthUtils
from integration.service.knowledge_cluster_service import KnowledgeClusterService


class KnowledgeClusterView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant = AuthUtils.get_tenant(request)
        clusters_with_folder_count = KnowledgeClusterService.get_clusters_with_folder_count(tenant)
        return Response({"code": HTTPStatus.OK, "message": clusters_with_folder_count})

    def post(self, request):
        tenant = AuthUtils.get_tenant(request)

        knowledge_id = request.POST.get("knowledge_id")

        # List of source and data path combination.
        data_folders = request.POST.get("data_folders")

