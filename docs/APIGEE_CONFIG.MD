# Apigee Documentation
[Discover](https://cloud.google.com/apigee/docs/api-platform/get-started/what-apigee)
[Getting Started](https://cloud.google.com/apigee/docs/api-platform/get-started/provisioning-intro)
[Develop](https://cloud.google.com/apigee/docs/api-platform/get-started/get-started)
[Develop Locally](https://cloud.google.com/apigee/docs/api-platform/local-development/overview)
[Publish](https://cloud.google.com/apigee/docs/api-platform/publish/publishing-overview)
[Monetize](https://cloud.google.com/apigee/docs/api-platform/monetization/overview)
[Administer](https://cloud.google.com/apigee/docs/api-platform/system-administration/users-roles-overview)
[Analyze](https://cloud.google.com/apigee/docs/api-platform/analytics/analytics-services-overview)
[API Monitoring](https://cloud.google.com/apigee/docs/api-monitoring)
[Advanced API Security](https://cloud.google.com/apigee/docs/api-security)
[Advanced API Operations](https://cloud.google.com/apigee/docs/aapi-ops)


# Deployment and Adding Proxies
[Google Cloud Platform Apigee Samples Github Repository](https://github.com/GoogleCloudPlatform/apigee-samples)

# [Eval Organization](https://cloud.google.com/apigee/docs/api-platform/get-started/eval-orgs) - Apigee (60 day trial)

## 1. [Setup with UI Wizard](https://apigee.google.com/setup)

* Enable APIs

* Networking - Establish private connection to Google services using VPC network 'default'

* Apigee evaluation organization - set location for analytics storage and runtime instance (<= 45 mins.)

* Access routing - No internet access or enabled internet access (VM instance group + GC Load Balancer [~$25/month](https://cloud.google.com/vpc/network-pricing#lb))

    I chose [1] enable internet access [2] use wildcard DNS service [3] default subnetwork

    34.49.250.10.nip.io

* GCP doesn't setup completely so next... [Set up with Apigee](https://apigee.google.com/welcome)

    and after a few minutes it seems like [ssl certs are provisioned](https://www.googlecloudcommunity.com/gc/Apigee/APIGEE-hello-world-doesn-t-work/m-p/550935)

## 2. [Apigee Console](https://apigee.google.com/edge) 

## 3. Setup Cloud Run Service to be run from Apigee Proxy.

[github sample](https://github.com/GoogleCloudPlatform/apigee-samples/tree/main/cloud-run)

[video](https://www.youtube.com/watch?v=oyFyPs0tg8Y)

1. Update env.sh with environment variables like apigee host and cloud run service name.

2. Enable the IAM API, Cloud Build API, Cloud Run API and Container Registry API. Assign Apigee Org admin, Cloud Run Admin , Service Account User and Admin role to the Cloud Build service account

```bash
gcloud services enable iam.googleapis.com cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/apigee.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/iam.serviceAccountAdmin"
```

3. Review how app/app.js builds a service.

*In the future, /app should be replaced with /produkter and the dockerfile should be swapped.*

It seems like this demo is configured to deploy a different app.

4. Review how cloudbuild.yaml file will build the cloud image and push container to container registry, then deploys image to cloud run, then apigee sa with invoker role accesses cloud run.

5. Trigger the build from the previous steps running:

```
gcloud builds submit --config cloudbuild.yaml . \
    --substitutions="_SERVICE=$CLOUD_RUN_SERVICE","_REGION=$CLOUD_RUN_REGION","_APIGEE_TEST_ENV=$APIGEE_ENV"
```

6. test if deployment was successful running:

```
curl -v -X GET https://$APIGEE_HOST/v1/samples/cloud-run-sample

ideally: curl -v -X GET https://$APIGEE_HOST/ or curl -v -X GET https://$APIGEE_HOST/set_produkt?alo hat
```

## Cleanup

If you want to clean up the artifacts from this example in your Apigee Organization, first source your `env.sh` script, and then run

```bash
./clean-up-cloud-run.sh
```