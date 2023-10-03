from django.db import models


class CredentialType(models.TextChoices):
    NONE = None
    OAUTH2 = 'oauth2'
