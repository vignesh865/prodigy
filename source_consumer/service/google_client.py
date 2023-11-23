import io
import logging
import os.path
import tempfile

import google.oauth2.credentials
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from integration.domain_models.source_type import SourceTypeValue


class GoogleClient:
    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v3'
    MAX_FOLDER_DEPTH = 3
    logger = logging.getLogger(__name__)

    @staticmethod
    def download_file(tenant_id, credential, file_id, name):
        try:
            # create drive api client
            service = GoogleClient.__build_client(credential)

            # pylint: disable=maybe-no-member
            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

        except HttpError as error:
            GoogleClient.logger.error(f"An error occurred for {tenant_id},"
                                      f" {SourceTypeValue.GOOGLE_DRIVE}, {file_id} : {error}")
            raise error

        saved_file_name = GoogleClient.save_file(file, name)
        return saved_file_name

    @staticmethod
    def __build_client(credential):
        google_credential = google.oauth2.credentials.Credentials(
            **credential)

        return googleapiclient.discovery.build(
            GoogleClient.API_SERVICE_NAME,
            GoogleClient.API_VERSION, credentials=google_credential)

    @staticmethod
    def save_file(file_bytes: io.BytesIO, file_name: str):
        file_name_without_ext = os.path.splitext(file_name)[0]
        extension = os.path.splitext(file_name)[1]

        temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False,
                                                prefix=file_name_without_ext, suffix=extension)
        temp_file.write(file_bytes.getbuffer())
        temp_file.close()

        return temp_file.name
