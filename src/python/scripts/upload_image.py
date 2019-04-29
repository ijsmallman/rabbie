from os.path import dirname, join
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_credentials():

    credentials_path = join(
        dirname(dirname(dirname(dirname(__file__)))),
        'secrets',
        'photos_api_credentials.json'
    )

    logger.debug(
        'Loading credentials from %s',
        credentials_path
    )

    with open(credentials_path, 'r') as f:
        credentials = json.load(f)
    
    return credentials


# # Credentials you get from registering a new application
# client_id = '<the id you get from google>.apps.googleusercontent.com'
# client_secret = '<the secret you get from google>'
# redirect_uri = 'https://your.registered/callback'

# # OAuth endpoints given in the Google API documentation
# authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
# token_url = "https://www.googleapis.com/oauth2/v4/token"
# scope = [
#     "https://www.googleapis.com/auth/userinfo.email",
#     "https://www.googleapis.com/auth/userinfo.profile"
# ]

# from requests_oauthlib import OAuth2Session
# google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

# # Redirect user to Google for authorization
# authorization_url, state = google.authorization_url(authorization_base_url,
#     # offline for refresh token
#     # force to always make user click authorize
#     access_type="offline", prompt="select_account")
# print 'Please go here and authorize,', authorization_url

# # Get the authorization verifier code from the callback url
# redirect_response = raw_input('Paste the full redirect URL here:')

# # Fetch the access token
# google.fetch_token(token_url, client_secret=client_secret,
#         authorization_response=redirect_response)

# # Fetch a protected resource, i.e. user profile
# r = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
# print r.content

if __name__ == '__main__':

    creds = load_credentials()
    a=2