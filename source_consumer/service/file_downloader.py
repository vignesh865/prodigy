from abc import abstractmethod, ABC

from source_consumer.models.ingest_message import IngestMessage


class FileDownloader(ABC):

    @abstractmethod
    def download_file(self, ingest_message: IngestMessage):
        pass
