from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.models.tenant import Tenant


class AppUser(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, blank=False)
