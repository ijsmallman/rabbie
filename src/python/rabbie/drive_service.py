import logging
from typing import List, Dict
from os.path import splitext, basename

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

MEME_TYPES = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.bmp': 'image/bmp'
}


class DriveServiceError(Exception):
    pass


class DriveService:

    def __init__(self, credentials: 'Credentials') -> None:
        self._service = build('drive', 'v3', credentials=credentials)

    def list_files(self) -> Dict[str, str]:
        """
        List all files in Google Drive

        Returns
        -------
        files: Dict[str, str]
            {file_id: file_name}

        Raises
        ------
        DriveServiceError
        """
        try:
            results = self._service.files().list(
                q='trashed=false',
                pageSize=10,
                fields="nextPageToken, files(id, name)"
            ).execute()
        except HttpError as e:
            logger.error("Failed to list all files in Drive. %s", e)
            raise DriveServiceError

        items = results.get('files', [])

        return {i['id']: i['name'] for i in items}

    def get_folder_id(self, folder_name) -> str:
        """
        Get folder ID

        Returns
        -------
        id: str

        Raises
        ------
        FileNotFoundError
        DriveServiceError
        """
        files = self.list_files()

        folder_id = None
        for id, name in files.items():
            if name == folder_name:
                folder_id = id
                break

        if folder_id is None:
            logger.warning("Failed to find folder %s", folder_name)
            raise FileNotFoundError

        return folder_id

    def create_folder(self, folder_name: str) -> str:
        """
        Create a folder in Google Drive

        Parameters
        ----------
        folder_name: str

        Returns
        -------
        folder_id: str

        Raises
        ------
        DriveServiceError
        """

        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
        }

        try:
            folder = self._service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
        except HttpError as e:
            logger.error("Failed to create folder. %s", e)
            raise DriveServiceError

        folder_id = folder.get('id')

        logger.info("Created folder with ID %s", folder_id)

        return folder_id

    def upload_image(self, file_path: str, folder_name: str=None) -> str:
        """
        Upload image to Google Drive

        Parameters
        ----------
        file_path: str
            Path to file to upload
        folder_name: str
            Name of folder on Google Drive. Create folder if it doesn't exist.
            Default (None): Store image in root directory

        Returns
        -------
        file_id: str
        """

        base_name = basename(file_path)
        file_name, extension = splitext(base_name)

        if folder_name is not None:
            try:
                folder_id = self.get_folder_id(folder_name)
            except FileNotFoundError:
                folder_id = self.create_folder(folder_name)
            parents = [folder_id]
        else:
            parents = []

        file_metadata = {
            'name': base_name,
            'parents': parents
        }

        try:
            meme_type = MEME_TYPES[extension]
        except KeyError:
            logger.error("Unrecognised image extension: %s", extension)
            raise DriveServiceError

        media = MediaFileUpload(
            file_path,
            mimetype=meme_type
        )

        try:
            file = self._service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
        except HttpError as e:
            logger.error("Failed to upload image. %s", e)
            raise DriveServiceError

        file_id = file.get('id')

        logger.info('Uploaded file with ID: %s', file_id)

        return file_id
