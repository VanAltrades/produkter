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