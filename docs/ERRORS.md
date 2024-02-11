## 2. Requests immediately timeout

```
textPayload: "The request has been terminated because it has reached the maximum request timeout. To change this limit, see https://cloud.google.com/run/docs/configuring/request-timeout"
```

## 3. Schemas/Texts from Sites hang infinitely

```
Failed to retrieve the page:
https://www.amazon.com/DOGIPOT-1402-30-Roll-Litter-Rolls/dp/B010VBMLKO. 

I tried to ommit those hanging urls (implemented in Sites)
It is designed to only return urls that loaded after 15 seconds
This did not work.
            try:
                for future in concurrent.futures.as_completed(futures, timeout=15):
                    i, text = future.result()
                    texts[i] = text
            except concurrent.futures.TimeoutError:
                # Handle the case where the timeout is reached
                print("Timeout reached. Not all tasks completed.")
```

SEEMS TO WORK LOCALLY BUT NOT IN CLOUD

```
503
{
"q":"CHECKPOINT CPY24MM"
}
{
"q":"COXREELS 117WT-1-200"
}

504
{
"q":"ILC KINGPIN EZGO / CUSHMAN / TEXTRON"
}
```

~~1. Previous Redis Integrations Causing Deployment to Fail~~

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

3. ~~Insecure connection~~

```
https://produkter-api-lwvz7mjmrq-uc.a.run.app/schemas?q=DOGIPOT%201402-30%20bags

?q=DOGIPOT 1402-30 bags

/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py:1099: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.walmart.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings


response = requests.get(url, headers=headers, verify=False)
^ this was sending a GET request to the URL with SSL verification disabled
it caused the warning so i did this for a solution:
response = requests.get(url, headers=headers)

However that ?q still hung infinitely. 
This is likely caused by one site hanging the parallelized scrapes.
To revert, I updated the concurrent requests to only return completed sites after 15 secs.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Use executor.map to parallelize the processing of links
            futures = [executor.submit(process_link, i, link) for i, link in enumerate(self.links)]

            # Wait for all tasks to complete and collect results with a timeout
            try:
                done, not_done = concurrent.futures.wait(futures, timeout=15, return_when=concurrent.futures.ALL_COMPLETED)
            except concurrent.futures.TimeoutError:
                # Handle the case where the timeout is reached
                print("Timeout reached. Not all tasks completed.")

            # Collect results from completed tasks
            for future in done:
                i, schema = future.result()
                schemas[i] = schema

        return schemas
```

4. ~~ValueError: invalid literal for int() with base 10: ''~~

```
I mislabeled REDISHOST and REDISPORT as REDIS_HOST and REDIS_PORT in my deployment script env vars.

I had to delete the cloud run/redis services and redeployed them with correct naming.
```

5. ~~Memory limit of 1024 MiB exceeded with 1099 MiB used. Consider increasing the memory limit, see https://cloud.google.com/run/docs/configuring/memory-limits~~ 

```gcloud run services update SERVICE_NAME --memory=1Gi```
