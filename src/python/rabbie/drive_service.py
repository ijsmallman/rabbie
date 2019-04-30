from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class DriveService:

    def __init__(self, creds: 'Credentials') -> None:
        self._service = build('drive', 'v3', credentials=creds)

    def list_files(self):
        # Call the Drive v3 API
        results = self._service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))