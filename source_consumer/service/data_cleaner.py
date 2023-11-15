from abc import ABC, abstractmethod

from source_consumer.models.ingest_message import IngestMessage


class DataCleaner(ABC):

    @abstractmethod
    def clean_document_pre_chunking(self, ingest_message: IngestMessage, document):
        pass

    @abstractmethod
    def clean_document_post_chunking(self, ingest_message: IngestMessage, document):
        pass
