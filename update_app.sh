#!/bin/bash
# to run: `chmod +x update_app.sh` then `./update_app.sh`

# Load environment variables from .env file
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | xargs)
else
  echo "Error: .env file not found."
  exit 1
fi

# docker tag gcr.io/$PROJECT_ID/$IMAGE_NAME gcr.io/$PROJECT_ID/$IMAGE_NAME

# gcloud auth configure-docker  # Authenticate Docker to push images to Container Registry
# docker push gcr.io/$PROJECT_ID/$IMAGE_NAME

# gcloud run deploy $SERVICE_NAME \
#   --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
#   --platform managed \
#   --allow-unauthenticated \
#   --region $REGION \
#   --set-env-vars CS_KEY=$CS_KEY,REDISHOST=$REDISHOST,REDISPORT=$REDISPORT

# BUILD + DEPLOY METHOD
# Build and push the Docker image to Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME  --project=$PROJECT_ID

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --allow-unauthenticated \
  --region $REGION \
  --set-env-vars CS_KEY=$CS_KEY,REDISHOST=$REDISHOST,REDISPORT=$REDISPORT