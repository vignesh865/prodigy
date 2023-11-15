from abc import ABC, abstractmethod

from source_consumer.models.ingest_message import IngestMessage


class DataChunker(ABC):

    @abstractmethod
    def chunk_document(self, ingest_message: IngestMessage, document):
        pass
