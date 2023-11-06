from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from source_poller.service.ingestion_service import IngestionService


class TriggerIngestionView(APIView):
    def get(self, request):
        tenant_id = request.GET.get('tenant_id')

        if tenant_id is None:
            IngestionService.trigger_ingestion_for_all_tenant()
            return Response(
                {"code": HTTPStatus.OK, "message": "Ingestion triggered for all the tenant and source combinations"})

        IngestionService.trigger_ingestion(tenant_id)
        return Response(
            {"code": HTTPStatus.OK, "message": f"Ingestion triggered for the tenant {tenant_id}"})
