import dacite

from integration.service.source_credential_service import SourceCredentialService
from source_consumer.models.google_file_metadata import GoogleFileMetadata
from source_consumer.models.ingest_message import IngestMessage
from source_consumer.service.file_downloader import FileDownloader
from source_consumer.service.google_client import GoogleClient


class GoogleFileDownloader(FileDownloader):

    def download_file(self, ingest_message: IngestMessage):
        credential = GoogleFileDownloader.get_credentials(ingest_message.tenant, ingest_message.source_type)
        file_metadata = dacite.from_dict(data_class=GoogleFileMetadata, data=ingest_message.file)

        file = GoogleClient.download_file(ingest_message.tenant, credential,
                                          file_metadata.id, file_metadata.name)
        return file, file_metadata.name

    @staticmethod
    def get_credentials(tenant_id, source_type_id):
        credential = SourceCredentialService.get_credential_source_id(tenant_id, source_type_id)
        return credential.credential
