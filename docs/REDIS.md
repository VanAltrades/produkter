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

## Steps to Deploy App to Cloud Run with Redis instance

1. Create Private Service Access VPC

2. Deploy Cloud Run Containerized API

3. Connect to New Redis after Deploying Cloud Run

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

## Deploy App (via .sh script `gcloud` command)

## Connect to New Redis after Deploying Cloud Run

[Connect to a Redis cache using Memorystore](https://cloud.google.com/run/docs/integrate/redis-memorystore) 

Update to the latest Google Cloud CLI:


```gcloud components update```

Create the integration:

```
gcloud beta run integrations create \
--type=redis \
--service=SERVICE \
--parameters=memory-size-gb=MEMORYSIZE
```

Replace

`SERVICE` with your Cloud Run service name.
`MEMORYSIZE` with the desired size in gigabytes of the cache. The default is 1 GB.

Wait up to 15 minutes, during which time a fully configured Redis cache is created and connected. In addition, a new Cloud Run revision is created, including networking configuration and environment variables needed for the Redis cache. When the process is complete, the following message is shown:

```
[redis] integration [redis-xxx] has been updated successfully.

To connect to the Redis instance, utilize the environment variables
REDISHOST and REDISPORT. These have been added to the Cloud Run service
for you.
```

You can check the status using `gcloud beta run integrations describe`

# Did not work methods

## Making a Serverless VPC 

If you're using Serverless VPC Access, create a connector. Be sure to use the same region and VPC network as the one used by the Redis instance. Make a note of the connector's name.

[configure serverless vpc access](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access#gcloud)

## [create cloud memorystore instance](https://cloud.google.com/memorystore/docs/redis/create-instance-console)


memorystore instance name: `redis-produkter-lite-memstore`

tier: `basic`

capacity: `1 GB`

network: `redis-vpc-network`

## Deploying Cloud Run and connecting to existing redis instance

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