from django.db import models

from authentication.models import AppUser
from authentication.models.tenant import Tenant
from integration.models.credential_type import CredentialType
from integration.models.source_type import SourceType


class OAuth2Redirection(models.Model):
    redirect_code = models.UUIDField(
        null=False,
        blank=False
    )

    redirect_data = models.JSONField()
