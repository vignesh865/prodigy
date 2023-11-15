from abc import ABC, abstractmethod

from source_consumer.models.ingest_message import IngestMessage


class DataRetriever(ABC):

    @abstractmethod
    def create_ensemble_retriever(self, ingest_message: IngestMessage):
        pass
