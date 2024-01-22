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

## [Create Direct VPC egress with a Shared VPC network](https://cloud.google.com/run/docs/configuring/shared-vpc-direct-vpc)

Redis Instances in MemoryStore require private IP address space via VPC.

Option 1. [Make shared VPC Host Project](https://console.cloud.google.com/networking/xpn/details?project=produkter-406316)


Option 2. [TRIED SERVERLESS BELOW BUT DIDN'T WORK WHEN CREATING MEMSTORE]

```
Server response: Unable to create/update instance. The allocated private IP address space is exhausted. For information on expanding the allocation, see https://cloud.google.com/vpc/docs/configure-private-services-access#modify-ip-range.
``` 

If you're using Serverless VPC Access, create a connector. Be sure to use the same region and VPC network as the one used by the Redis instance. Make a note of the connector's name.

[configure serverless vpc access](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access#gcloud)

within: [console > vpc network > serverless vpc access](https://console.cloud.google.com/networking/connectors/list?project=produkter-406316)

name: `redis-produkter-lite-conn`

region: `us-central1`

network: `default`

subnet: `10.128.0.0/20`

min instances: `2`

max instance: `3`

```
gcloud compute networks vpc-access connectors create CONNECTOR_NAME \
--network VPC_NETWORK \
--region REGION \
--range IP_RANGE
```

## [create cloud memorystore instance](https://cloud.google.com/memorystore/docs/redis/create-instance-console)


memorystore instance name: `redis-produkter-lite-memstore`

tier: `basic`

capacity: `1 GB`

network: `default`

```
gcloud redis instances describe INSTANCE_ID --region REGION --format "value(authorizedNetwork)"
```

[connect redis to cloud run](https://cloud.google.com/memorystore/docs/redis/connect-redis-instance-cloud-run)


## Deploying App to Cloud Run with Redis instance

Then build and deploy the cloud run instance.

If using memorystore, be sure `--network`, `--subnet`, `--set-env-vars` are defined in .sh script or gcloud command.