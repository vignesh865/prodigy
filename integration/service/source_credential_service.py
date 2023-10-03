from authentication.models import Tenant, AppUser
from integration.models import SourceCredentials, SourceType

from integration.models.credential_type import CredentialType


class SourceCredentialService:

    @staticmethod
    def is_credentials_present(tenant_id, source_type):
        return SourceCredentials.objects.filter(tenant=tenant_id,
                                                source_type=SourceType(source_type)).exists()

    @staticmethod
    def save_google_drive_credentials(tenant_id, user_id, credentials):
        SourceCredentialService.save_credentials(tenant_id, user_id, credentials,
                                                 SourceType.GOOGLE_DRIVE, CredentialType.OAUTH2)

    @staticmethod
    def save_credentials(tenant_id, user_id, credentials, source_type, credential_type):
        credential = SourceCredentialService.credentials_to_dict(credentials)

        source_credentials = SourceCredentials.objects.create(tenant=Tenant(id=tenant_id),
                                                              source_type=source_type,
                                                              credential_type=credential_type,
                                                              credential=credential,
                                                              updated_by=AppUser(user_id))

        source_credentials.save()

    @staticmethod
    def get_all_integrated_sources(tenant_id):
        values = SourceCredentials.objects.filter(tenant=tenant_id).values('source_type')
        return [data.get("source_type") for data in values]

    @staticmethod
    def credentials_to_dict(credentials):
        return {'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}
