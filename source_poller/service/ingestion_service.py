import itertools
import logging

from django.conf import settings
from django.core.exceptions import BadRequest
from django.forms import model_to_dict

from authentication.models import Tenant
from integration.domain_models.source_type import SourceTypeValue
from integration.models.data_folders import DataFolders
from source_poller.service.google_ingestion_service import GoogleIngestionService
from source_poller.service.kafka_producer_service import KafkaProducerService


class IngestionService:
    logger = logging.getLogger(__name__)
    SOURCE_INGESTION_TOPIC = settings.SOURCE_POLLER_KAFKA_CONFIG["sourceIngestionTopic"]

    @staticmethod
    def trigger_ingestion_for_all_tenant():
        tenant_ids = Tenant.objects.all().values('id')
        for tenant_id in tenant_ids:
            IngestionService.trigger_ingestion(tenant_id)

    @staticmethod
    def trigger_ingestion(tenant_id):
        data_folders = DataFolders.objects.filter(tenant_id=tenant_id).order_by('knowledge_id')

        for knowledge_id, group in itertools.groupby(data_folders, lambda item: item.knowledge_id):
            logging.info(f"Started Ingestion for the cluster - {knowledge_id}")
            IngestionService.trigger_ingestion_for_cluster(tenant_id, list(group))
            logging.info(f"Completed Ingestion for the cluster - {knowledge_id}")

        logging.info(f"Completed Ingestion for the tenant - {tenant_id}")

    @staticmethod
    def trigger_ingestion_for_cluster(tenant_id, data_folders: list):

        source_types = [data_folder.source_type for data_folder in data_folders]
        source_type_id_dict = {data.id: SourceTypeValue[data.source_type] for data in source_types}

        for data_folder in data_folders:
            source_type = source_type_id_dict.get(data_folder.source_type.id)
            ingestion_service = IngestionService.get_ingestion_service_by_source(source_type)
            files = ingestion_service.get_files(tenant_id, data_folder.source_type, data_folder)

            # Send each file as message in Kafka topic
            IngestionService.send_files(data_folder, files)

    @staticmethod
    def send_files(data_folder, files):
        producer = KafkaProducerService.get_instance()
        data_folder_dict = model_to_dict(data_folder)
        for file in files:
            data_folder_dict["file"] = file
            producer.send_message(IngestionService.SOURCE_INGESTION_TOPIC, data_folder_dict)

    @staticmethod
    def get_ingestion_service_by_source(source_type: SourceTypeValue):

        if source_type == SourceTypeValue.GOOGLE_DRIVE:
            return GoogleIngestionService

        raise BadRequest(f"Unsupported source - {source_type}")
