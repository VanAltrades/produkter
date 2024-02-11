#!/bin/bash
# to run: `chmod +x deploy_app.sh` then `./deploy_app.sh`

# be sure to update dockerfile to correct file first

# Set your project ID
# PROJECT_ID=produkter-406316

# # Set your image name
# IMAGE_NAME=produkter-image

# # Set your desired service name
# SERVICE_NAME=produkter-api

# MEMORYSIZE=1

# Load environment variables from .env file
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | xargs)
else
  echo "Error: .env file not found."
  exit 1
fi

# gcloud iam service-accounts create SERVICE_ACCOUNT_NAME --display-name "Produkter API Service Account"
# gcloud projects add-iam-policy-binding PROJECT_ID --member=serviceAccount:SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com --role=roles/run.admin

# delete existing to avoid errors if applicable
gcloud run services delete produkter-api --region us-central1
gcloud beta run integrations delete redis-1

# Build and push the Docker image to Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME  --project=$PROJECT_ID

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --allow-unauthenticated \
  --memory=1Gi \
  --region $REGION \
  --set-env-vars CS_KEY=$CS_KEY,REDISHOST=$REDISHOST,REDISPORT=$REDISPORT
# OK Deploying new service... Done.
#   OK Creating Revision...
#   OK Routing traffic...
#   OK Setting IAM Policy...
# Done.

# Create the Redis integration for Cloud Run (only need to deploy this once):
gcloud beta run integrations create \
--type=redis \
--service=$SERVICE_NAME \
--region $REGION

# --parameters=memory-size-gb=$MEMORYSIZE # this parameter seems to have been sunset
# \  Creating new Integration... Deployment started. This process will continue even if your terminal session is interrupted.
#   OK Saving Configuration for Integration... You can check the status with `gcloud beta run integrations describe redis-1`
#   \  Configuring Integration... This might take up to 10 minutes.
#   .  Configuring Cloud Run Service...
#   .  Configuring Cloud Memorystore...
#   \  Configuring VPC Connector...