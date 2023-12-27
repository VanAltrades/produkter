from config.app_secrets import CS_KEY, SA_CREDENTIALS

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