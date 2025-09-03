import google.auth
from google.auth.transport.requests import Request
from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

load_dotenv()

# https://developers.google.com/custom-search/v1/overview#api_key
CS_KEY = os.getenv("CS_KEY")


# https://cloud.google.com/iam/docs/service-account-overview
# Load default credentials from deployment's project
def load_credentials_default(scopes=["https://www.googleapis.com/auth/cse"]):
    try:
        credentials, _ = google.auth.default(scopes=scopes)
        credentials.refresh(Request())
        # return credentials.token
        return credentials
    except GoogleAuthError as e:
        print(f"Failed to authenticate: {e}")
        return None


def load_credentials_from_file():
    SA_CREDENTIALS_PATH=os.getenv("SA_CREDENTIALS_PATH")
    return service_account.Credentials.from_service_account_file(
        SA_CREDENTIALS_PATH, 
        scopes=["https://www.googleapis.com/auth/cse"]
    )


try:     # authenticate via json file on local
    SA_CREDENTIALS = load_credentials_from_file()
except:        # default GOOGLE_APPLICATION_DEFAULT
    SA_CREDENTIALS = load_credentials_default()