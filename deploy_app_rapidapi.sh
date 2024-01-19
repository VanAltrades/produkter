#!/bin/bash
# to run: `chmod +x deploy.sh` then `./deploy.sh`

# Set your project ID
PROJECT_ID="produkter-406316"

# Set your image name
IMAGE_NAME="produkter-rapidapi"

# Set your desired service name
SERVICE_NAME="produkter-rapidapi"

# Set your desired region
REGION="us-central1"

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
  --region $REGION \
  --allow-unauthenticated \
  --update-env-vars CS_KEY=$CS_KEY