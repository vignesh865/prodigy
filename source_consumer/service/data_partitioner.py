from abc import ABC, abstractmethod

from source_consumer.models.ingest_message import IngestMessage


class DataPartitioner(ABC):

    @abstractmethod
    def partition(self, ingest_message: IngestMessage, local_file_url: str) -> list:
        pass
