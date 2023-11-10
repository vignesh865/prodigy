import json
import uuid

from confluent_kafka import Producer
from django.conf import settings


class KafkaProducerService:
    __instance = None

    def __init__(self):
        if KafkaProducerService.__instance is not None:
            raise Exception(f"{__name__} - This class is a singleton!")

        kafka_config = settings.SOURCE_POLLER_KAFKA_CONFIG["kafka"]
        self.producer = Producer(kafka_config)

        KafkaProducerService.__instance = self

    @staticmethod
    def value_serializer(message: dict):
        return json.dumps(message).encode('utf-8')

    def send_message(self, topic, message, key=None):
        if not key:
            key = str(uuid.uuid4())

        return self.producer.produce(topic, KafkaProducerService.value_serializer(message), key)

    @staticmethod
    def get_instance(reinit=False):
        """ Static access method. """

        if reinit:
            KafkaProducerService.__instance = None

        if KafkaProducerService.__instance is None:
            KafkaProducerService()

        return KafkaProducerService.__instance
