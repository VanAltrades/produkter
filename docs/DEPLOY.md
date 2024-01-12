# Produkter Lite

From gcloud command line in repo directory:

```
gcloud builds submit --tag gcr.io/ProjectID/produkter-lite  --project=ProjectID
<!-- API [cloudbuild.googleapis.com] not enabled on project [produkter-406316]. -->

gcloud run deploy --image gcr.io/ProjectID/produkter-lite --platform managed  --project=ProjectID --allow-unauthenticated
<!-- The following APIs are not enabled on project [produkter-406316]:run.googleapis.com -->
```

## Helpful gcloud commands

```
gcloud projects list
```