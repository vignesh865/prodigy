from source_consumer.consumers.base_consumer import BaseConsumer
from source_consumer.service.source_ingest_service import SourceIngestService


class SourceIngestConsumer(BaseConsumer):
    def process_message(self, key, message):
        SourceIngestService.process_message(key, message)
