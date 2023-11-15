from source_consumer.models.ingest_message import IngestMessage
from source_consumer.service.data_chunker import DataChunker
from unstructured.chunking.title import chunk_by_title


class UnstructuredDataChunker(DataChunker):

    def chunk_document(self, ingest_message: IngestMessage, elements):
        chunks = chunk_by_title(elements)
        return chunks
