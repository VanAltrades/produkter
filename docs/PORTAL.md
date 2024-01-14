# Deploy Drupal Portal
[Drupal Developer Portal Deployment Script](https://github.com/GoogleCloudPlatform/apigee-samples/tree/main/drupal-developer-portal/apiproxy)
[Drupal portal solution](https://cloud.google.com/apigee/docs/api-platform/publish/intro-portals)
[Drupal on GCP deployment video](https://www.youtube.com/watch?v=GeLqhPX9MPE)

from drupal-developer-portal git repo...

1. export environment variables and source shell script 

```
##env.sh
export PROJECT="produkter-XXX"
export APIGEE_HOST="XX.XX.nip.io"
export APIGEE_ENV="eval"

source ./env.sh
```

2. Deploy Apigee resources (proxy & product) required for the Drupal portal

```
./deploy-drupal-developer-portal.sh
```

NOTE: This script creates an API Proxy and API product. It does not, however, create the developer portal. We will create and test that manually

3. Enable Apigee Developer Portal Kickstart from [GCP Marketplace](https://console.cloud.google.com/marketplace?_ga=2.40868130.1832225602.1705169573-2128967561.1693853298)

Click Launch

4. Follow [instructions](https://cloud.google.com/apigee/docs/api-platform/publish/drupal/get-started-cloud-marketplace) to Deploy

* make new Service Account (drupal-sa)

* enable https

* click deploy (~1 hour)

5. Save credentials during deployment

    * Site address (HTTPS)

    * Username

    * Password

```
Username:	admin
Password:	gvTSKnayCay6R9WT
```


* Deployment name = sample-drupal-developer-portal
# Monetizing Client Requests
[Apigee Drupal Developer Portal - Monetization Module](https://github.com/apigee/apigee-m10n-drupal)
[GCP Documentation on Apigee Monetization](https://cloud.google.com/apigee/docs/api-platform/monetization/overview#:~:text=Using%20Apigee's%20monetization%20feature%2C%20you,API%20revenue%20with%20the%20developers.)