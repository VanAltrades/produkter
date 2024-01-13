# Produkter Lite

make sure `debug=False` for deployment

From gcloud command line in repo directory:

```
gcloud builds submit --tag gcr.io/ProjectID/produkter-lite  --project=ProjectID
<!-- API [cloudbuild.googleapis.com] not enabled on project [produkter-406316]. -->

gcloud run deploy --image gcr.io/ProjectID/produkter-lite --platform managed  --project=ProjectID --allow-unauthenticated

gcloud run deploy --image gcr.io/ProjectID/produkter-lite --platform managed  --project=ProjectID --allow-unauthenticated --update-env-vars SA_CREDENTIALS_JSON="$(cat ./src/config/dukt_sa.json)"
<!-- The following APIs are not enabled on project [produkter-406316]:run.googleapis.com -->
```

## Helpful gcloud commands

```
gcloud projects list
gcloud iam service-accounts list

```