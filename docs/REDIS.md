# REDIS INTEGRATION

[tutorial video](https://www.youtube.com/watch?v=_8lJ5lp8P0U&t=1s)

## Local Install

[install windows](https://redis.io/docs/install/)

1. [install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

2. [install Redis](https://redis.io/docs/install/install-redis/install-redis-on-windows/)

## Running Redis on WSL

start Redis server

```
sudo service redis-server start
```

connect to Redis server

```
redis-cli 

127.0.0.1:6379> ping
PONG
```

## Running Redis from Python Package

[pypi](https://pypi.org/project/redis/)

## Deploying App to Cloud Run with Redis instance

[gcloud doc](https://cloud.google.com/memorystore/docs/redis/connect-redis-instance-cloud-run)