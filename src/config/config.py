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




# from config.app_secrets import CS_KEY, SA_CREDENTIALS

# TODO: database url if needed
# implement:    https://levelup.gitconnected.com/implement-api-caching-with-redis-flask-and-docker-step-by-step-9139636cef24
# deploy:       https://cloud.google.com/memorystore/docs/redis/connect-redis-instance-cloud-run#python

# import os

# class BaseConfig(object):
    # CS_KEY = os.environ['CS_KEY']
    # SA_CREDENTIALS = os.environ['SA_CREDENTIALS']
       
    # CACHE_TYPE = os.environ['CACHE_TYPE']
    # CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    # CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    # CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
    # CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    # CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']