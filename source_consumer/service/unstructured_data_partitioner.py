from source_consumer.models.ingest_message import IngestMessage
from source_consumer.service.data_partitioner import DataPartitioner
from unstructured.partition.auto import partition


class UnstructuredDataPartitioner(DataPartitioner):

    def partition(self, ingest_message: IngestMessage, local_file_url: str):
        return partition(local_file_url)
