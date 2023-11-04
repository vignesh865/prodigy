import google.oauth2.credentials
import googleapiclient.discovery

from integration.service.source_credential_service import SourceCredentialService


class GoogleIntegrationService:
    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v3'

    @staticmethod
    def load_folders(tenant_id, source_type, search_term="a"):
        saved_credential = GoogleIntegrationService.load_credentials(tenant_id, source_type).credential
        credentials = google.oauth2.credentials.Credentials(
            **saved_credential)

        drive = googleapiclient.discovery.build(
            GoogleIntegrationService.API_SERVICE_NAME,
            GoogleIntegrationService.API_VERSION, credentials=credentials)

        query = f"mimeType = 'application/vnd.google-apps.folder' and name contains '{search_term}'"
        return drive.files().list(q=query).execute()

    @staticmethod
    def load_credentials(tenant_id, source_type):
        return SourceCredentialService.get_credential(tenant_id, source_type)
