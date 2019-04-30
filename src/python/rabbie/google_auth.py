import os
import pickle
from os.path import join, dirname
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SECRETS_PATH = join(
    dirname(dirname(dirname(dirname(__file__)))),
    'secrets'
)
TOKEN_FILENAME = "token.pickle"
CREDENTIALS_FILENAME = "credentials.json"


class GoogleAuthError(Exception):
    pass


class GoogleAuth:

    def __init__(self) -> None:

        token_path = join(SECRETS_PATH, TOKEN_FILENAME)
        credentials_path = join(SECRETS_PATH, CREDENTIALS_FILENAME)

        creds = None
        if os.path.exists(token_path):
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path,
                    SCOPES
                )
                creds = flow.run_local_server()

            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))