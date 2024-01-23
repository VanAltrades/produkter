#!/bin/bash
# to run: `chmod +x deploy_.sh` then `./deploy_.sh`

# be sure to update dockerfile to correct file first

# Set your project ID
PROJECT_ID=produkter-406316

# Set your image name
IMAGE_NAME=produkter-lite-redis

# Set your desired service name
SERVICE_NAME=produkter-lite-redis

MEMORYSIZE=1

# NETWORK="projects/produkter-406316/global/networks/redis-vpc-network"

# Load environment variables from .env file
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | xargs)
else
  echo "Error: .env file not found."
  exit 1
fi

# Build and push the Docker image to Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME  --project=$PROJECT_ID

# Deploy to Cloud Run

gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --allow-unauthenticated \
  --region $REGION \
  --set-env-vars CS_KEY=$CS_KEY,REDISHOST=$REDIS_IP,REDISPORT=$REDIS_PORT


# gcloud run deploy $SERVICE_NAME \
#   --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
#   --platform managed \
#   --allow-unauthenticated \
#   --region $REGION \
#   --network $NETWORK \
#   --subnet $SUBNET \
#   --set-env-vars CS_KEY=$CS_KEY,REDISHOST=$REDIS_IP,REDISPORT=$REDIS_PORT

# gcloud run deploy \
# --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
# --platform managed \
# --allow-unauthenticated \
# --region $REGION \
# --network $NETWORK \
# --subnet $SUBNET \
# --set-env-vars CS_KEY=$CS_KEY,REDISHOST=$REDIS_IP,REDISPORT=$REDIS_PORT

# gcloud run deploy --image gcr.io/$PROJECT_ID/$IMAGE_NAME --platform managed --allow-unauthenticated --region $REGION --network $NETWORK --subnet $SUBNET --set-env-vars CS_KEY=$CS_KEY,REDISHOST=$REDIS_IP,REDISPORT=$REDIS_PORT

# Create the Redis integration for Cloud Run:
gcloud beta run integrations create \
--type=redis \
--service=$SERVICE_NAME \
--region $REGION
--parameters=memory-size-gb=$MEMORYSIZE