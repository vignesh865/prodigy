import json
import uuid

from kafka3 import KafkaProducer


class KafkaProducerService:
    __instance = None
    BOOTSTRAP_SERVERS = 'localhost:9092'

    def __init__(self):
        if KafkaProducerService.__instance is not None:
            raise Exception(f"{__name__} - This class is a singleton!")

        key_serializer = str.encode
        self.producer = KafkaProducer(key_serializer=key_serializer,
                                      value_serializer=KafkaProducerService.value_serializer,
                                      bootstrap_servers=KafkaProducerService.BOOTSTRAP_SERVERS)

        KafkaProducerService.__instance = self

    @staticmethod
    def value_serializer(message):
        return json.dumps(message).encode('utf-8')

    def send_message(self, topic, message, key=None):
        if not key:
            key = str(uuid.uuid4())

        return self.producer.send(topic, message, key).get(60)

    @staticmethod
    def get_instance(reinit=False):
        """ Static access method. """

        if reinit:
            KafkaProducerService.__instance = None

        if KafkaProducerService.__instance is None:
            KafkaProducerService()

        return KafkaProducerService.__instance
