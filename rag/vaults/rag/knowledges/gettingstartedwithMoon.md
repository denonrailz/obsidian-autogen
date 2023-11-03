---
_id: 
version: "0.1"
type: knowledge
---
# Getting started with Moon

## Overview
Moon is a browser automation solution compatible with [Selenium](https://www.w3.org/TR/webdriver/), [Cypress](https://www.cypress.io/), [Playwright](https://playwright.dev/), and [Puppeteer](https://pptr.dev/) using [Kubernetes](https://kubernetes.io/).

## Useful resources
- [Offcial documentation](https://aerokube.com/moon/latest/)
- Free dedicated support channels on Telegram:
    - [RU](https://t.me/aerokube)
    - [EN](https://t.me/aerokube_moon)

## Quick start using Service Catalog
To get started with Moon:
1. In Google Cloud console, go to [Service Catalog](https://console.cloud.google.com/catalog), enter the word **Moon** in the search box, and then select **[CloudApp] Aerokube Moon**.<br>
To log in, use the EPAM account (Your_Name@epam.com) and select your project (EPM-< tenant >-ANTHOS) to deploy the Moon solution.<br>
![assets/moon_1.png](assets/moon_1.png)
2. Read the description, and then select **DEPLOY**.<br>
![assets/moon_2.png](assets/moon_2.png)
3. Configure the parameters, and then select **PREVIEW AND DEPLOY**.<br>
![assets/moon_3.png](assets/moon_3.png)

| Parameter | Description | Example |
| ----------- | ----------- | ----------- |
| Deployment name | Readable unique name for moon deployment. | epm-acme-moon |
| cluster_name | GKE Cluster name. Copy it from the [Kubernetes clusters](https://console.cloud.google.com/kubernetes/list/overview) page. | epm-paas-b-europe-west3-cl1 |
| namespace | [Kubernetes namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) to deploy moon resources. | moon |
| hostname | Desired hostname on the existing domain for GKE. Copy the domain from the [certificates](https://console.cloud.google.com/security/ccm/list/lbCertificates) page. | epm-paas-b-cl1-default-lb.eu.gcp.epm-paas.projects.epam.com |
| has_license | If you have a license for more than 4 browsers, select the checkbox. | True | 
| license | If you have a license for more than 4 browsers, copy it to this field. | It looks like base64 string: `YnIzWTJYL2...<stripped>...1EQjk=` |
| chart_version | On the [releases](https://github.com/aerokube/charts/releases) page, see the available charts for Moon v2.*.*. | 2.5.3 |

4. Select **DEPLOY** when the button gets highlighted.<br>
:warning: Wait until the deployment is completed.<br>
![assets/moon_4.png](assets/moon_4.png)
5. To check the installation in GKE, go to the [terminal](https://cloud.google.com/shell/docs/launching-cloud-shell) using [kubectl CLI](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl) or see [Workloads](https://console.cloud.google.com/kubernetes/workload/overview) in Google Cloud console.<br>
PODs are running.<br>

```
$ kubectl -n moon get pods
NAME                    READY   STATUS    RESTARTS   AGE
moon-858fc68855-lcczp   3/3     Running   0          3m24s
```

HTTPRoute resource is created.<br>

```
$ kubectl -n moon get httproute
NAME   HOSTNAMES                                                              AGE
moon   ["moon.epm-paas-b-cl1-default-lb.eu.gcp.epm-paas.projects.epam.com"]   5m21s
```

Make sure endpoints respond using cURL (EPAM VPN is required).<br>

```
$ host moon.epm-paas-b-cl1-default-lb.eu.gcp.epm-paas.projects.epam.com
moon.epm-paas-b-cl1-default-lb.eu.gcp.epm-paas.projects.epam.com has address 10.82.13.31

$ curl -I -k https://moon.epm-paas-b-cl1-default-lb.eu.gcp.epm-paas.projects.epam.com
HTTP/1.1 200 OK

$ curl -k https://moon.epm-paas-b-cl1-default-lb.eu.gcp.epm-paas.projects.epam.com/wd/hub
Moon: 2.5.3
```

## Updating and deprovisioning
For more information on how to update a terraform deployment, see the [official Google documentation](https://cloud.google.com/service-catalog/docs/view-and-launch#update_terraform).<br>

For more information on how to deprovision a terraform deployment, see the [official Google documentation](https://cloud.google.com/service-catalog/docs/view-and-launch#deprovision_a_terraform_deployment).

## Troubleshooting
### Issues during deployment
Make sure the Cloud Build service account has at least **Kubernetes Engine Developer** role. To check it, go to [Cloud Build settings](https://console.cloud.google.com/cloud-build/settings/service-account).

### Issues with DNS resolution
- Make sure that EPAM VPN is enabled.
- Make sure that the existing DNS records are used, and check the domain from pre-configured [certificates](https://console.cloud.google.com/security/ccm/list/lbCertificates).
- Make sure that [Gateway](https://cloud.google.com/kubernetes-engine/docs/concepts/gateway-api) is installed on your cluster.<br>

```
$ kubectl get gateway -A
NAMESPACE          NAME               CLASS         ADDRESS       PROGRAMMED   AGE
epm-paas-gateway   default-internal   gke-l7-rilb   10.82.13.31   True         5d22
```
For more information Kubernetes Gateway API, see the [official documentation](https://gateway-api.sigs.k8s.io/). 


