# Produkter Lite

From gcloud command line in repo directory:

```
gcloud builds submit --tag gcr.io/ProjectID/produkter-lite  --project=ProjectID

gcloud run deploy --image gcr.io/ProjectID/produkter-lite --platform managed  --project=ProjectID --allow-unauthenticated
```