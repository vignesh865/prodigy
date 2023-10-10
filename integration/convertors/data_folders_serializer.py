from rest_framework import serializers

from integration.models.data_folders import DataFolders


class DataFoldersSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = DataFolders
        fields = ['id', 'folder_name', 'folder_reference', 'source_type', 'knowledge', 'created_by']
