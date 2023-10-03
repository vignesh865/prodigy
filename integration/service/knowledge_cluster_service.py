from django.db.models import Count

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
