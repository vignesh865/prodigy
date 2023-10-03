from django.db import models

from authentication.models import AppUser, Tenant


class KnowledgeCluster(models.Model):

    cluster_name = models.CharField(
        max_length=150,
        null=False,
        blank=False
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, blank=False)

    created_by = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, blank=False)
    # updated_by = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, blank=False)
