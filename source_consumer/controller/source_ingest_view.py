from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from source_consumer.service.source_ingest_service import SourceIngestService


class SourceIngestView(APIView):

    def post(self, request):
        key = request.data.get('key')
        message = request.data.get('message')

        SourceIngestService.process_message(key, message)

        return Response(
            {"code": HTTPStatus.OK, "message": f"Processed given message"})
