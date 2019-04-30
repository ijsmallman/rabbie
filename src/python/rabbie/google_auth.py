import os
import pickle
import logging
from os.path import join, dirname
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SECRETS_PATH = join(
    dirname(dirname(dirname(dirname(__file__)))),
    'secrets'
)
TOKEN_FILENAME = "token.pickle"
CREDENTIALS_FILENAME = "credentials.json"


logger = logging.getLogger(__name__)


class GoogleAuthError(Exception):
    pass


def google_auth(headless: bool = False) -> 'Credentials':

    token_path = join(SECRETS_PATH, TOKEN_FILENAME)
    credentials_path = join(SECRETS_PATH, CREDENTIALS_FILENAME)

    credentials = None
    if os.path.exists(token_path):
        try:
            with open(token_path, 'rb') as token:
                credentials = pickle.load(token)
        except IOError as e:
            logger.error("Failed to load api token. %s", e)
            raise GoogleAuthError

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if headless:
            logger.error("Failed to authorise application")
            raise GoogleAuthError

        else:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path,
                    SCOPES
                )
                credentials = flow.run_local_server()
    
            # Save the credentials for the next run
            try:
                with open(token_path, 'wb') as token:
                    pickle.dump(credentials, token)
            except IOError as e:
                logger.error("Failed to save api token to %s. %s", token_path, e)

    return credentials
