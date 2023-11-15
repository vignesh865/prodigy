from django.core.exceptions import BadRequest

from integration.domain_models.source_type import SourceTypeValue
from integration.models import SourceType
from source_consumer.models.ingest_message import IngestMessage
from source_consumer.service.data_chunker import DataChunker
from source_consumer.service.data_cleaner import DataCleaner
from source_consumer.service.data_partitioner import DataPartitioner
from source_consumer.service.data_updator import DataUpdator
from source_consumer.service.file_downloader import FileDownloader
from source_consumer.service.google_file_downloader import GoogleFileDownloader
from source_consumer.service.qdrant_data_updater import QdrantDataUpdator
from source_consumer.service.unstructured_data_chunker import UnstructuredDataChunker
from source_consumer.service.unstructured_data_cleaner import UnstructuredDataCleaner
from source_consumer.service.unstructured_data_partitioner import UnstructuredDataPartitioner


class PipelineOrchestrator:

    def __init__(self, ingest_message: IngestMessage):
        self.ingest_message = ingest_message

    def get_downloader(self) -> FileDownloader:
        return PipelineOrchestrator.__get_instance_by_source(self.ingest_message.source_type)

    def get_partitioner(self) -> DataPartitioner:
        return UnstructuredDataPartitioner()

    def get_cleaner(self) -> DataCleaner:
        return UnstructuredDataCleaner()

    def get_chunker(self) -> DataChunker:
        return UnstructuredDataChunker()

    def get_updator(self) -> DataUpdator:
        return QdrantDataUpdator()

    @staticmethod
    def __get_instance_by_source(source_type_id):
        source_type = SourceType.objects.get(id=source_type_id).source_type
        if source_type == SourceTypeValue.GOOGLE_DRIVE.name:
            return GoogleFileDownloader()

        raise BadRequest(f"Unsupported source - {source_type}")
