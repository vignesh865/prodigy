from enum import Enum

from django.db import models


class SourceType(models.Model):
    source_type = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    source_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    readable_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
