import logging

import google.oauth2.credentials
import googleapiclient.discovery
from google.api_core.exceptions import BadRequest

from integration.models import SourceCredentials
from integration.models.data_folders import DataFolders


class GoogleIngestionService:
    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v3'
    MAX_FOLDER_DEPTH = 3
    logger = logging.getLogger(__name__)

    @staticmethod
    def get_files(tenant_id, source_type_id, data_folder: DataFolders):
        credential = SourceCredentials.objects.filter(tenant=tenant_id,
                                                      source_type=source_type_id)

        if len(credential) == 0:
            raise BadRequest(f"Credential not present for {tenant_id} and {source_type_id}")

        credential = credential[0].credential

        files = GoogleIngestionService.load_files(data_folder, credential)
        return files

    @staticmethod
    def load_files(data_folder: DataFolders, credential: dict):
        google_credential = google.oauth2.credentials.Credentials(
            **credential)

        drive = googleapiclient.discovery.build(
            GoogleIngestionService.API_SERVICE_NAME,
            GoogleIngestionService.API_VERSION, credentials=google_credential)

        files = []
        GoogleIngestionService.load_files_recursively(drive, data_folder.folder_name, data_folder.folder_reference, 0,
                                                      files)
        return files

    @staticmethod
    def load_files_recursively(drive, start_folder_name, parent_folder_ref, depth=0, files=[]):

        if depth > GoogleIngestionService.MAX_FOLDER_DEPTH:
            GoogleIngestionService.logger.error(
                f"Depth exceeded for {start_folder_name} folder, Curbing at {parent_folder_ref}")
            return

        query = f"'{parent_folder_ref}' in parents"
        folder_mime_type = "application/vnd.google-apps.folder"

        # files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = drive.files().list(q=query, pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change

                if file.get("mimeType") == folder_mime_type:
                    GoogleIngestionService.load_files_recursively(drive, start_folder_name, file.get("id"), depth + 1,
                                                                  files)
                    continue

                files.append(file)

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
