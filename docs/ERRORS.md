1. Previous Redis Integrations Causing Deployment to Fail

When running:
```
# Create the Redis integration for Cloud Run:
gcloud beta run integrations create \
--type=redis \
--service=$SERVICE_NAME \
--region $REGION
```

```
ERROR: (gcloud.beta.run.integrations.create) INVALID_ARGUMENT: The request was invalid: Invalid Config: service allows 1 binding(s), not 2
- '@type': type.googleapis.com/google.rpc.BadRequest
  fieldViolations:
  - field: Application_Config
- '@type': type.googleapis.com/google.rpc.RequestInfo
  requestId: a8ed9855e5a0d910
```

Solution idea:

Remove Existing Integration:

If there is an existing Redis integration, consider removing it before trying to create a new one. You can do this using the gcloud beta run integrations delete command.

```
$ gcloud beta run integrations list

# outputs:
To make this the default region, run `gcloud config set run/region us-central1`.

   INTEGRATION  TYPE   REGION       SERVICE
+  redis-1      redis  us-central1  produkter-lite-redis
+  redis-2      redis  us-central1  produkter-api

# then I run:
$ gcloud beta run integrations delete redis-1
$ gcloud beta run integrations delete redis-2

```

Then I re-run integration (final .sh command)

2. Requests immediately timeout

```
textPayload: "The request has been terminated because it has reached the maximum request timeout. To change this limit, see https://cloud.google.com/run/docs/configuring/request-timeout"
```

3. Insecure connection

```
https://produkter-api-lwvz7mjmrq-uc.a.run.app/schemas?q=DOGIPOT%201402-30%20bags

/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py:1099: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.walmart.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings

```

4. ValueError: invalid literal for int() with base 10: ''