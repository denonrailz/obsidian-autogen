---
_id: 
version: "0.1"
type: knowledge
---
# Load balance traffic using Gateway API

## Overview
GKE Gateway API is the GCP implementation of [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/) using the [GKE Gateway controller](https://cloud.google.com/kubernetes-engine/docs/concepts/gateway-api#gateway_controller). GKE Gateway API provides an alternative to traditional approaches like Ingress or Service to enable more advanced functionalities for exposing applications in GKE.

In CloudApp Kubernetes Enterprise, we've prepared the following configurations:<br>
- **Gateway controller** is deployed in a single-cluster mode with the preinstalled default certificates and a wildcard DNS name.<br>
- **Static IP address** is used for DNS and Load Balancer configuration.<br>
- **Default certificates** are configured [Let's Encrypt](https://letsencrypt.org/) certificates, but you can add custom ones, if necessary.<br>
- **Default wildcard DNS name** is managed by CloudApp Engine, but you can add a custom one, if necessary.<br>
- **Cloud Application LoadBalancer** is managed by the Gateway controller.

Gateway API lets different application environments, running in different Namespaces, share the same IP address, DNS domain, certificates, or paths for fine-grained routing between services. Gateways provide administrators with control over which Namespaces can route for a specific domain.

The following diagram illustrates how Gateway API works in CloudApp Enterprise Kubernetes.<br>
![assets/loadbalancetraffic_1.png](assets/loadbalancetraffic_1.png)

## How to use GKE Gateway API
> GKE Gateway API is already preconfigured in each cluster with HTTP and HTTPS Regional Application load balancers. Besides, there are created wildcard domain names and Let's Encrypt certificates that last for 90 days with regular rotation by the CloudApp Engine team.<br>
![assets/loadbalancetraffic_2.png](assets/loadbalancetraffic_2.png)

To use GKE Gateway API:<br>
1. To expose your application through Gateway, create a HTTPRoutes custom resource in your application namespace.<br>
One of the benefits of using Gateway is sharing one gateway for many routers or tenants in the cluster. Thus, you can create many HTTP Routes for different applications and attach them to one Gateway. Before applying `httproute`, make sure you have deployed the workload and created the service.<br><br>
This is an example of an application Hostname from the Ingress chapter.<br>

```
kind: HTTPRoute
apiVersion: gateway.networking.k8s.io/v1beta1
metadata:
  name: my-application
  namespace: my-namespace
spec:
  parentRefs:
  - kind: Gateway
    name: default-internal
    namespace: epm-paas-gateway
  hostnames:
  - hostname-app.epm-paas-b-cl1-default-lb.eu.gcp.epm-paas.projects.epam.com
  rules:
  - backendRefs:
    - name: hostname
      port: 80
```

To use this example as a template in your environment, do the following:<br>
- Use your name and namespace.<br>
- Define the hostname with the correct wildcard domain name (see the *How to use GKE Gateway API* note above).<br>
- Define rules that can be the default backend as in the example or a more complex set of rules—with routing by `path` and `headers`.<br>For more detailed information about HTTPRoute, see the [official Project page](https://gateway-api.sigs.k8s.io/api-types/httproute).<br>
- Leave the **parentRefs** section where Gateway binding is defined as is.

2. Verify that the HTTPRoute has been deployed.<br>
`kubectl describe httproute my-application`
3. Verify that the HTTPRoute is bound to Gateway.<br>
`kubectl describe gateway default-internal -n epm-paas-gateway`

## Useful commands
Use the following commands to:<br>
1. Get certificate information.<br>

```
$gcloud compute ssl-certificates list --project or2-msq-epm-paas-b-t1iylu
NAME                                    TYPE          CREATION_TIMESTAMP             EXPIRE_TIME                    REGION        MANAGED_STATUS
epm-paas-b-us-east4-cl2-lb-default      SELF_MANAGED  2023-10-05T15:14:22.136-07:00  2024-01-03T13:14:19.000-08:00  us-east4
epm-paas-b-europe-west3-cl1-lb-default  SELF_MANAGED  2023-10-06T00:21:34.052-07:00  2024-01-03T22:21:21.000-08:00  europe-west3
```

Additionally, you can get detailed information on certain certificates where you can find the load balancer domain name.<br>

```
$gcloud compute ssl-certificates describe  --project or2-msq-epm-paas-b-t1iylu --region europe-west3 epm-paas-b-europe-west3-cl1-lb-default --flatten="subjectAlternativeNames[0]"
---
  '*.epm-paas-b-cl1-default-lb.eu.gcp.epm-paas.projects.epam.com'
```

2. View static IPs.<br>

```
$gcloud compute addresses list --project or2-msq-epm-paas-b-t1iylu --regions europe-west3
NAME                                    ADDRESS/RANGE  TYPE      PURPOSE                  NETWORK  REGION        SUBNET                             STATUS
epm-paas-b-europe-west3-cl1-lb-default  10.82.13.31    INTERNAL  SHARED_LOADBALANCER_VIP           europe-west3  epm-paas-eu-west3-poc-main-subnet  IN_USE
```



