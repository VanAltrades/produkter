# Produkter Lite

## Configure Compute Engine Service Account for Cloud Run
```
XXXX-compute@developer.gserviceaccount.com

Grant Service Account Token Creator. This role allows the service account to create short-lived credentials.
roles/iam.serviceAccountTokenCreator


```

make sure `debug=False` for deployment

## Deploy with gcloud

From deploy_app_lite.sh file in repo directory:

Update environment vars in .sh script. Then...

```
$ chmod +x deploy.sh
$ ./deploy.sh
```

or from gcloud command line in repo directory:

```
gcloud builds submit --tag gcr.io/ProjectID/produkter-lite  --project=ProjectID
gcloud builds submit --tag gcr.io/produkter-406316/produkter-lite  --project=produkter-406316

gcloud run deploy --image gcr.io/ProjectID/produkter-lite --platform managed  --project=ProjectID --allow-unauthenticated
gcloud run deploy --image gcr.io/produkter-406316/produkter-lite --platform managed  --project=produkter-406316 --allow-unauthenticated
```

## Set Environment Variables Once Deployed
```
> Edit & Deploy New Revision
> Variables & Secrets
> Add Variable
[CS_KEY, PORT]
```

## Helpful gcloud commands

```
gcloud projects list
gcloud iam service-accounts list

```