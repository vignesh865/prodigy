import dacite
from django.core.exceptions import BadRequest

from integration.domain_models.source_type import SourceTypeValue
from integration.models import SourceCredentials
from source_consumer.models.google_file_metadata import GoogleFileMetadata
from source_consumer.models.ingest_message import IngestMessage
from source_consumer.service.google_client import GoogleClient
from source_consumer.service.file_downloader import FileDownloader


class GoogleFileDownloader(FileDownloader):

    def download_file(self, ingest_message: IngestMessage):
        credential = GoogleFileDownloader.get_credentials(ingest_message.tenant)
        file_metadata = dacite.from_dict(data_class=GoogleFileMetadata, data=ingest_message.file)

        file = GoogleClient.download_file(ingest_message.tenant, credential, file_metadata.id)
        return file

    @staticmethod
    def get_credentials(tenant_id):
        credential = SourceCredentials.objects.filter(tenant=tenant_id,
                                                      source_type=SourceTypeValue.GOOGLE_DRIVE)

        if len(credential) == 0:
            raise BadRequest(f"Credential not present for {tenant_id} and {SourceTypeValue.GOOGLE_DRIVE}")

        return credential[0].credential
