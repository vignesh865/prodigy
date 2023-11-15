import logging
import threading

from django.conf import settings

from source_consumer.consumers.source_ingest_consumer import SourceIngestConsumer


class ConsumerInitiator:
    @staticmethod
    def init():
        ingest_data_source_config = settings.SOURCE_CONSUMER_KAFKA_CONFIG["ingest-data-source"]
        ingest_data_source_consumer = SourceIngestConsumer(ingest_data_source_config.get("kafka"),
                                                           [ingest_data_source_config.get("consumerTopic")],
                                                           ingest_data_source_config.get("consumerCommitBatch"))

        logging.info("Main    : before creating thread")
        x = threading.Thread(target=ingest_data_source_consumer.start, daemon=True)
        logging.info("Main    : before running thread")
        x.start()
