from django.db import models

from authentication.models import AppUser
from integration.models import SourceType
from integration.models.knowledge_cluster import KnowledgeCluster


# It is a combination of data path and source type. For example: , FolderA in GOOGLE_DRIVE
class DataFolders(models.Model):
    folder_name = models.CharField(
        max_length=150,
        null=False,
        blank=False
    )

    # This can be some unique id, or path, or anything which refers based on the source type.
    folder_reference = models.CharField(
        max_length=150,
        null=False,
        blank=False
    )

    source_type = models.ForeignKey(SourceType, on_delete=models.DO_NOTHING, blank=False)
    knowledge = models.ForeignKey(KnowledgeCluster, on_delete=models.DO_NOTHING, blank=False)

    created_by = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, blank=False)
    # updated_by = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, blank=False)
