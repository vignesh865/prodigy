from enum import Enum

from django.db import models


class SourceType(models.TextChoices):
    GOOGLE_DRIVE = 'google_drive'
    MICROSOFT_ONEDRIVE = 'microsoft_onedrive'
    CONFLUENCE = 'confluence'
