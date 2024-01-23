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

## Prerequisite Steps to Deploy App to Cloud Run with Redis instance

## [Create private service access VPC](https://cloud.google.com/vpc/docs/configure-private-services-access#modifying-connection)

Redis Instances in MemoryStore require private IP address space via VPC.

Save private ip for later --ranges

[Solution?](https://cloud.google.com/knowledge/kb/unable-to-create-redis-instance-with-private-service-access-due-to-allocated-private-ip-address-space-being-exhausted-000004746)

```
$ gcloud services vpc-peerings update \
    --service=servicenetworking.googleapis.com \
    --ranges=10.128.0.0/20 \
    --network=redis-vpc-network \
    --project=produkter-406316 \
    --force
```
If you're using Serverless VPC Access, create a connector. Be sure to use the same region and VPC network as the one used by the Redis instance. Make a note of the connector's name.

[configure serverless vpc access](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access#gcloud)

## [create cloud memorystore instance](https://cloud.google.com/memorystore/docs/redis/create-instance-console)


memorystore instance name: `redis-produkter-lite-memstore`

tier: `basic`

capacity: `1 GB`

network: `redis-vpc-network`

## Deploying App to Cloud Run with Redis instance

connect to new redis after deploying cloudrun: [Connect to a Redis cache using Memorystore](https://cloud.google.com/run/docs/integrate/redis-memorystore) 

Connecting to an existing redis instance did not work (steps below) because the --network and --subnet arguments provided in the link below are not recognized.

```
# gcloud run deploy \
# --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
# --platform managed \
# --allow-unauthenticated \
# --region $REGION \
# --network $NETWORK \
# --subnet $SUBNET \
# --set-env-vars CS_KEY=$CS_KEY,REDISHOST=$REDIS_IP,REDISPORT=$REDIS_PORT
```

[connect redis to cloud run](https://cloud.google.com/memorystore/docs/redis/connect-redis-instance-cloud-run)

```
gcloud redis instances describe INSTANCE_ID --region REGION --format "value(authorizedNetwork)"

> projects/produkter-406316/global/networks/redis-vpc-network
```

Then build and deploy the cloud run instance.