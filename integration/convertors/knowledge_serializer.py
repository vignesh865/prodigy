from rest_framework import serializers

from integration.models.knowledge_cluster import KnowledgeCluster


class KnowledgeClusterSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = KnowledgeCluster
        fields = ['id', 'cluster_name', 'tenant', 'created_by']
