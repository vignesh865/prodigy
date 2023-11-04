from django.core.exceptions import BadRequest
from django.db.models import Count

from integration.convertors.data_folders_serializer import DataFoldersSerializer
from integration.models import SourceType
from integration.models.data_folders import DataFolders
from integration.models.knowledge_cluster import KnowledgeCluster


class KnowledgeClusterService:

    @staticmethod
    def get_clusters_with_folder_count(tenant):
        knowledge_clusters = list(KnowledgeCluster.objects.filter(tenant=tenant).values("id", "cluster_name"))
        knowledge_clusters_dict = {cluster.get("id"): cluster.get("cluster_name") for cluster in knowledge_clusters}

        data_folders = DataFolders.objects.filter(knowledge_id__in=list(knowledge_clusters_dict.keys())).values(
            "knowledge_id").annotate(
            num_folders=Count("id"))

        for data_folder in data_folders:
            data_folder["knowledge_cluster_name"] = knowledge_clusters_dict.get(data_folder.get("knowledge_id"))

        return data_folders

    @staticmethod
    def create_knowledge_cluster(tenant, user, cluster_name, data_folders):
        source_name_id_dict = KnowledgeClusterService.get_source_name_id_dict(
            [data.get("source_name") for data in data_folders])
        knowledge_cluster = KnowledgeCluster(cluster_name=cluster_name, tenant=tenant, created_by=user)
        knowledge_cluster.save()

        for data in data_folders:
            data["knowledge"] = knowledge_cluster.id
            data["source_type"] = source_name_id_dict.get(data["source_name"])
            data["created_by"] = user.id

        data_folders_model = DataFoldersSerializer(data=data_folders, many=True)
        if not data_folders_model.is_valid():
            raise BadRequest(data_folders_model.errors)

        data_folders_model.save()

        return data_folders_model.data

    @staticmethod
    def get_source_name_id_dict(source_names):
        sources = SourceType.objects.filter(source_name__in=source_names)
        return {data.source_name: data.id for data in sources}
