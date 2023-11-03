---
_id: 3309d38fa132a1cbeac2368a3
version: "0.1"
type: knowledge
---
# Getting started with CloudApp Kubernetes Enterprise

This page URL: https://docs.cloudapp.epam.com/#/gettingstartedwithCloudAppKubernetesEnterprise

## Before you begin
Before you start working with CloudApp Kubernetes Enterprise, get familiar with the following recommendations:
### Learn Google Cloud fundamentals
As an [Application Team engineer](https://docs.cloudapp.epam.com/#/responsibilities) (developer or DevOps engineer), you need to gain basic Google Cloud knowledge. We recommend two learning paths where you can choose the best option for you: 

|Options|Google Cloud Skills Boost for Partners links|Estimations|
|---|---|---|
|Fast track path|Required:  <br>1. [Google Cloud Fundamentals: Core Infrastructure](https://partner.cloudskillsboost.google/course_templates/60)  <br>2. [Architecting with Google Kubernetes Engine: Foundations](https://partner.cloudskillsboost.google/course_templates/32)  <br>3. [Architecting with Google Kubernetes Engine: Workloads](https://partner.cloudskillsboost.google/course_templates/34)  <br>Optional:  <br>1. [Architecting with Google Kubernetes Engine: Production](https://partner.cloudskillsboost.google/course_templates/33)|About 10 full-time days (min)  <br>  <br>  <br>  <br>  <br>About 5 full-time days (min)|
|Full path|1. [Associate Cloud Engineer Certification Learning Path](https://partner.cloudskillsboost.google/journeys/69)  <br>2. [Architecting with Google Kubernetes Engine: Production](https://partner.cloudskillsboost.google/course_templates/33)|About 35 full-time days (min)|

Make sure that you have approval for learning from your PM or DM.
For more information on GCP Certification and training for EPAM, see [GCP Certification](https://kb.epam.com/display/EPMCEDU/GCP+Certification).
### Learn architectural aspects of CloudApp Kubernetes Enterprise
Architectural aspects of CloudApp Kubernetes Enterprise include the following items: 
#### Regions
Google Cloud supports a huge list of regions, but we use the regions where EPAM has Interconnects to their on-premise infrastructure. For CloudApp Kubernetes Enterprise, the following regions are available:
- **EU-WEST3**—Frankfurt, Germany
- **US-EAST**—Ashburn, Virginia, and North America
#### Networking
With Anthos architecture, every project leverages shared VPC that has network subnets available from the EPAM network, and vice versa. The Client doesn't need to request additional subnets or EPAM VPN via our support portal, and can use subnets shared with the project. You can check it in the VPC networking service view, for example:  
    ![assets/gettingstartedwithCKE_1.png](https://docs.cloudapp.epam.com/assets/gettingstartedwithCKE_1.png)
    
#### GKE Autopilot
By default, we provide GKE Autopilot clusters as the most cost-effective way, where you don't need to manage autoscalers or choose node pools. After activating CloudApp Kubernetes Enterprise (Anthos Fleet), the GKE Autopilot cluster(s) should be available in both tabs:
- Kubernetes Engine/Clusters
- Anthos/Fleet management/Clusters  
GKE Autopilot mode is a hands-off, fully managed Kubernetes platform that manages your cluster’s underlying compute infrastructure (without you needing to configure or monitor)—while still delivering a complete Kubernetes experience.
For more information, see [Autopilot is now GKE’s default mode of operation — here’s what that means for you](https://cloud.google.com/blog/products/containers-kubernetes/gke-autopilot-is-now-default-mode-of-cluster-operation).
#### Anthos 
Anthos (GKE Enterprise) and Google Cloud use the concept of a fleet to simplify managing multi-cluster deployments. A fleet provides a way to logically group and normalize Kubernetes clusters, helping us uplevel management from individual clusters to entire groups of clusters.
For more information, see [GKE Enterprise (Anthos) fleets management](https://cloud.google.com/anthos/fleet-management/docs).
## Get started with CloudApp Kubernetes Enterprise

To get started with CloudApp Kubernetes Enterprise, do the following
### Step 1. Activate CloudApp
To activate CloudApp Kubernetes Enterprise in GCP, submit the [support request](https://support.epam.com/ess?id=sc_cat_item&sys_id=f7325a8a97035190386e3a871153af6e&name=EPAMPaaS%2FCloudAppEngineMaintenanceAndConsulting&sysparm_copy_vars=%7B%22u_Action%22:%22Consulting%20about%20EPAM%20CloudApp%20Engine%22%7D). For that, use the following information:
#### Request title
EPAM PaaS / CloudApp Engine maintenance and consulting
#### Type of assistance
Consulting about EPAM CloudApp Engine
#### Project name
Project needs to enter Project name (*for example, EPM-PaaS*)
#### Required consultation
I need a Google Anthos Consultation
#### Comments
1. **Estimated monthly cost** - project needs to specify an estimated monthly cost
2. **Cluster configuration**  - specify cluster configuration, selecting the suitable option. If you're new to Public Clouds, select default cluster configuration. You'll get a configured cluster in Europe with the [Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview) cluster type. If you're experienced with Public Clouds, indicate the required cluster configuration: 
	1. a. Cluster number (example: 1, 2, ..., n)  
	2. b. Cluster region (Europe or America)  
	3. c. Cluster type ([Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview) or [Standard](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-zonal-cluster))*
3. If you need to deploy several clusters for your Project, the data for each cluster must be specified separately.
4. If neither of the options suits you, request a Product Owner consultation and provide details.

### Step 2. Log in to Google Cloud console
After the Anthos Fleet activation, you can connect to the GCP project via [Google Cloud console](https://console.cloud.google.com/) with EPAM domain credentials by choosing a particular GCP Project at the top of it (for example, EPM-PAAS).  
    
### Step 3. Set up gcloud CLI
To manage Google Cloud (gcloud) from CLI, do the following:
1. Install google-cloud-sdk. For more details, see the [Install the gcloud CLI](https://cloud.google.com/sdk/docs/install) guide
2. Authorize the gcloud CLI
```shell
gcloud init
gcloud info
gcloud projects list
```
For more details, see the [Authorize the gcloud CLI](https://cloud.google.com/sdk/docs/authorizing) guide
3. Configure the gcloud CLI
```
    `gcloud config list`  
    `gcloud config set project or2-msq-epm-paas-t1iylu`
```
For more details, see [gcloud config set](https://cloud.google.com/sdk/gcloud/reference/config/set)
4. Start onboarding