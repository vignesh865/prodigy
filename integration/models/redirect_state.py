from django.db import models

from integration.models.source_type import SourceType


class RedirectState(models.Model):
    state = models.CharField(primary_key=True, max_length=50)
    source_type = models.ForeignKey(SourceType, on_delete=models.DO_NOTHING, blank=False)
    redirect_data = models.JSONField()
    is_complete = models.BooleanField(default=False)
