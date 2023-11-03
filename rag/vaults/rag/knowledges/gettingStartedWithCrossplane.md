---
_id: 
version: "0.1"
type: knowledge
---
# Getting started with Crossplane

## Overview
Crossplane is a powerful Kubernetes operator that seamlessly integrates with your cluster. By extending the Kubernetes API, Crossplane enables you to access and manage native cloud services from leading providers such as GCP, AWS, and Azure, all from within your GKE clusters. With Crossplane, there's no need to define resources outside your cluster, simplifying your resource management and enhancing your cloud-native workflow. Crossplane empowers you to select and use the right cloud service that best suits your specific requirements.

## Quick start using Service Catalog
1. Go to [Service Catalog](https://console.cloud.google.com/catalog) in GCP Console, type `Crossplane` in the Search field, and select **[Anthos] Crossplane** solution
2. Click **Deploy** on the **Details** page. Configure parameters and click **Preview and Deploy**

| Parameter | Description |Example|
| ----------- | ----------- |---|
|Deployment name|Human readable unique name for deployment|crossplane-epm-acme|
|cluster_name|GKE Cluster name in text. Copy it from [Kubernetes clusters page](https://console.cloud.google.com/kubernetes/list/overview)|epm-paas-b-europe-west3-cl1|
|namespace|[Kubernetes namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) there to deploy Crossplane resources|upbound-system|
|crossplane_version|Crossplane [helm chart](https://github.com/crossplane/crossplane/tree/master/cluster/charts/crossplane) version. All available version could be checked in [releases](https://github.com/crossplane/crossplane/releases)|1.13.2|
|gcp_provider_version|Which version of Crossplane GCP Provider to install. All available version in [releases page](https://github.com/upbound/provider-gcp/releases)|0.37.0|
|enable_gcp_provider|Must be toggled if you plan to create GCP resources|true|

3. Make sure the preview completes successfully and click **Deploy**
4. Go to the terminal and verify installation in GKE by using the [kubectl CLI](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl) tool or by checking the [Workloads](https://console.cloud.google.com/kubernetes/workload/overview) page in GCP Console.<br>
✅ PODs are running:
```
$ kubectl -n upbound-system get pods
NAME                                                        READY   STATUS    RESTARTS   AGE
crossplane-bf99d468c-tzqms                                  1/1     Running   0          3m50s
crossplane-rbac-manager-8647648466-9wxpm                    1/1     Running   0          3m50s
upbound-provider-family-gcp-883052ff3af4-54fb6f485d-s9drk   1/1     Running   0          3m21s
upbound-provider-gcp-sql-0d2121e07a87-75968cd4c4-ccw72      1/1     Running   0          3m11s
```

Now, Crossplane is ready to handle CloudSQL claims and accommodate additional Crossplane providers.

## Updating and Deprovisioning
- For information on updating, please read this [document](https://cloud.google.com/service-catalog/docs/view-and-launch#update_terraform).
- To learn how to deprovision, refer to this [instruction](https://cloud.google.com/service-catalog/docs/view-and-launch#deprovision_a_terraform_deployment).

## Troubleshooting

**Issues during deployment**

To address deployment issues, please make sure that the Cloud Build service account has been assigned the **Kubernetes Engine Developer** role. You can verify and configure this role in the [GCP Console's Cloud Build settings](https://console.cloud.google.com/cloud-build/settings/service-account) page.



