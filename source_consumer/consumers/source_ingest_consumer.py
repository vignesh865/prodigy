from source_consumer.consumers.base_consumer import BaseConsumer


class SourceIngestConsumer(BaseConsumer):
    def process_message(self, key, message):
        print(key, message)
