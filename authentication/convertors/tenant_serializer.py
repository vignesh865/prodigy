from rest_framework import serializers

from authentication.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Tenant
        fields = ['id', 'tenant_name', 'is_active', 'date_joined']
