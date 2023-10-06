from django.db import models

from authentication.models import AppUser
from authentication.models.tenant import Tenant
from integration.models.credential_type import CredentialType
from integration.models.source_type import SourceType


class SourceCredentials(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, blank=False)
    source_type = models.ForeignKey(SourceType, on_delete=models.DO_NOTHING, blank=False)
    credential_type = models.CharField(
        max_length=25,
        choices=CredentialType.choices,
        null=False,
        blank=False
    )

    credential = models.JSONField()
    updated_by = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, blank=False)
