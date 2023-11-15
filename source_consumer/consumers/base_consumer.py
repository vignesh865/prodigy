import json
import logging

from confluent_kafka import Consumer, KafkaError, KafkaException


class BaseConsumer:
    logger = logging.getLogger(__name__)

    def __init__(self, config, topic, min_commit_count,
                 key_serializer=None, value_serializer=None):
        self.running = False
        self.min_commit_count = min_commit_count
        self.topic = topic
        self.consumer = Consumer(config)

        self.key_serializer = key_serializer
        self.value_serializer = value_serializer

        if not key_serializer:
            self.key_serializer = lambda key: key.decode('utf-8')

        if not value_serializer:
            self.value_serializer = lambda value: json.loads(value.decode('utf-8'))

    def start(self):
        self.running = True
        try:
            self.consumer.subscribe(self.topic, on_assign=self.assign_callback)

            msg_count = 0
            while self.running:
                msg = self.consumer.poll(timeout=5)
                if msg is None: continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        BaseConsumer.logger.info('%% %s [%d] reached end at offset %d\n' %
                                                 (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:

                    self.process_message(self.key_serializer(msg.key()), self.value_serializer(msg.value()))
                    msg_count += 1
                    if msg_count % self.min_commit_count == 0:
                        self.consumer.commit(asynchronous=False)
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    @staticmethod
    def assign_callback(consumer, partition):
        BaseConsumer.logger.info(f"Consumer assigned - {partition}")

    def stop(self):
        self.running = False

    def process_message(self, key, message):
        pass
