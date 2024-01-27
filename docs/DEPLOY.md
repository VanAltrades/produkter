# Produkter Lite

## Deployment Checklist

.py checklist

* debug=False

.sh checklist

* image name is correct?
* service name is correct?
* memorystore memory size is correct?
* --set-env-vars set correctly from .env file?

.env checklist

* applicable environment variables called from .sh exist in .env?

Dockerfile checklist

* app file in /src is named accurately based on what you want deployed?

```[app:app, app_lite_redis:app, app_rapidapi:app, ...]```

.dockerignore checklist

* secret files under /config ignored?
* /docs ignores?
* unused /templates ignored?
* any other bloated /dirs or files ignored?

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