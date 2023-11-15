import dacite
from langchain.embeddings import SentenceTransformerEmbeddings

from source_consumer.consumers.base_consumer import BaseConsumer
from source_consumer.models.ingest_message import IngestMessage
from source_consumer.service.pipeline_orchestrator import PipelineOrchestrator


class SourceIngestConsumer(BaseConsumer):
    def process_message(self, key, message):

        ingest_message = dacite.from_dict(data_class=IngestMessage, data=message)

        po = PipelineOrchestrator(ingest_message)
        file_url = po.get_downloader().download_file(ingest_message)
        elements = po.get_partitioner().partition(ingest_message, file_url)

        cleaner = po.get_cleaner()
        cleaned_elements = cleaner.clean_document_pre_chunking(ingest_message, elements)
        chunked_elements = po.get_chunker().chunk_document(ingest_message, cleaned_elements)
        cleaned_chunks = cleaner.clean_document_post_chunking(ingest_message, chunked_elements)

        embedding_model = SentenceTransformerEmbeddings()
        po.get_updator().update_data(embedding_model, "", cleaned_chunks)



