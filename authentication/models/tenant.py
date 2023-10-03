from django.db import models
from django.utils import timezone


class Tenant(models.Model):
    tenant_name = models.CharField(
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        max_length=150,
        verbose_name="tenant_id",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)