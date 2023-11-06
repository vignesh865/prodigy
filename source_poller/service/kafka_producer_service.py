import json

from kafka3 import KafkaProducer


class KafkaProducerService:
    __instance = None
    BOOTSTRAP_SERVERS = 'localhost:1234'

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
        future = self.producer.send(topic, message, key)
        return future.get(60)

    @staticmethod
    def get_instance(reinit=False):
        """ Static access method. """

        if reinit:
            KafkaProducerService.__instance = None

        if KafkaProducerService.__instance is None:
            KafkaProducerService()

        return KafkaProducerService.__instance
