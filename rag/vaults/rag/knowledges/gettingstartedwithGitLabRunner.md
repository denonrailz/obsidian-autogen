---
_id: 
version: "0.1"
type: knowledge
---
# Getting started with GitLab Runner

## Overview
GitLab Runner is a build instance that is used to run jobs. GitLab Runner with the Kubernetes executor can be used to run CI/CD jobs in your Kubernetes cluster. With this runner, you can easily integrate your GitLab project with your Kubernetes environment to enable automated builds, testing, and deployment of your code. The runner supports dynamic provisioning of pods and can scale up or down based on the usage requirements of your jobs.

## GitLab Runner installation
To set up GitLab Runner: 
1. In your Git repository, select **Settings** (1)> **CI/CD** (2) > **Runners** (3)> **Expand** (4).<br>
![assets/gitlabrunner_1new.png](assets/gitlabrunner_1new.png)
2. In the **Runners** section, go to **Specific runners** (1) > **Set up a specific runner manually** (2), and then take the required steps.<br>
![assets/gitlabrunner_2.png](assets/gitlabrunner_2.png)<br>
:information_source: To register the runner with GitLab, copy the GitLab URL and registration token from step 2.
3. Log in to [Google Cloud console](https://console.cloud.google.com/), and then go to [Anthos clusters](https://console.cloud.google.com/anthos/clusters).<br>
Alternatively,  log in to [Google Cloud console](https://console.cloud.google.com/), and then go to **Navigation menu** (1) > **Anthos** (2) > **Clusters** (3).<br>
![assets/gitlabrunner_3new.png](assets/gitlabrunner_3new.png)<br>
:information_source: For further steps, you need to know the name of the cluster registered in the fleet. Copy it to the clipboard and save the cluster name where you are going to install the GitLab runner.<br>
![assets/gitlabrunner_4new.png](assets/gitlabrunner_4new.png)
4. Go to [Service Catalog Solution](https://console.cloud.google.com/catalog) and select the desired solution.<br>
![assets/gitlabrunner_7new.png](assets/gitlabrunner_7new.png)<br>
Alternatively, search for **service catalog**, select the corresponding folder, and then select the desired solution.<br>
![assets/gitlabrunner_6new.png](assets/gitlabrunner_6new.png)
5. Read the description, and then select **DEPLOY**.<br>
![assets/gitlabrunner_6new.png](assets/gitlabrunner_6new.png)
6. Fill in all the required fields, update the fields with default values if needed, and then select **PREVIEW AND DEPLOY**.<br>
![assets/gitlabrunner_9new.png](assets/gitlabrunner_9new.png)
7. Select **DEPLOY** when the button gets highlighted.<br>
:warning: Wait until the deployment is completed.<br>
![assets/gitlabrunner_10new.png](assets/gitlabrunner_10new.png)
8. After the deployment is successful, validate the runner in GitLab UI.<br>
![assets/gitlabrunner_12new.png](assets/gitlabrunner_12new.png)

## Kubernetes API access
By default, gitlab-runner is provisioned with the enabled API access to the namespace where gitlab-runner is created (you have the [edit](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles) role for the namespace).<br>
![assets/gitlabrunner_13new.png](assets/gitlabrunner_13new.png)

To use gitlab-runner for deployment to another namespace, enable <code>clusterWideAccess</code>  and use the **Overwrite** functionality. For more information, see the official GitLab documentation:<br>
- [Overwrite the Kubernetes namespace](https://docs.gitlab.com/runner/executors/kubernetes.html#overwrite-the-kubernetes-namespace)
- [Overwrite the Kubernetes default service account](https://docs.gitlab.com/runner/executors/kubernetes.html#overwrite-the-kubernetes-default-service-account)

To enable <code>clusterWideAccess</code>:
1. Go to **Terraform deployments** and select the desired deployment.<br>
![assets/gitlabrunner_14new.png](assets/gitlabrunner_14new.png)
2. Select **MODIFY**.<br>
![assets/gitlabrunner_15new.png](assets/gitlabrunner_15new.png)
3. Enable <code>clusterWideAccess</code>, and then select **PREVIEW AND DEPLOY**.<br>
![assets/gitlabrunner_16new.png](assets/gitlabrunner_16new.png)
4. Select **DEPLOY** when the button gets highlighted.<br>
:warning: Wait until the deployment is completed.<br>
![assets/gitlabrunner_17new.png](assets/gitlabrunner_17new.png)
5. In the desired namespace, create a [Kubernetes service account](https://kubernetes.io/docs/concepts/security/service-accounts/).<br> Let's assume we'll create a new service account and bind it to the <code>edit</code> ClusterRole (for all cases, we recommend using least privilege rules) in the <code>cloudapp-demo</code> namespace.<br>

```
# kubectl create namespace cloudapp-demo
# kubectl create serviceaccount gitlab-runner-executor -n cloudapp-demo
# kubectl create rolebinding gitlab-runner-executor --clusterrole=edit --serviceaccount=cloudapp-demo:gitlab-runner-executor -n cloudapp-demo
```
6. To interact with the namespace, add special variables to the stage description in the <code>.gitlab-ci.yaml</code> file: <code>KUBERNETES_NAMESPACE_OVERWRITE</code> and <code>KUBERNETES_SERVICE_ACCOUNT_OVERWRITE</code>.<br>

```
list-pods:
  stage: deploy
  image: bitnami/kubectl
  variables:
    KUBERNETES_NAMESPACE_OVERWRITE: cloudapp-demo
    KUBERNETES_SERVICE_ACCOUNT_OVERWRITE: gitlab-runner-executor
  script:
    - kubectl get pods -n cloudapp-demo
```
```
Executing "step_script" stage of the job script 00:01
$ kubectl get pods -n cloudapp-demo
NAME                                                   READY   STATUS    RESTARTS   AGE
runner-z2cqxw-i-project-170846-concurrent-2-09uka0za   2/2     Running   0          48s
runner-z2cqxw-i-project-170846-concurrent-3-bfmpz1cr   0/2     Pending   0          46s
```
## GitLab CI distributed cache
To speed up the time it takes to download language dependencies, use a distributed cache.<br>
For more information about cache, see [Caching in GitLab CI/CD](https://docs.gitlab.com/ee/ci/caching/).

The distributed cache is disabled by default. To enable cache:
1. Go to **Terraform deployments** and select the desired deployment.<br>
![assets/gitlabrunner_14new.png](assets/gitlabrunner_14new.png)
2. Select **MODIFY**.<br>
![assets/gitlabrunner_15new.png](assets/gitlabrunner_15new.png)
3. Enable <code>runner_cache_enabled</code>, and then select **PREVIEW AND DEPLOY**.<br>
![assets/gitlabrunner_18new.png](assets/gitlabrunner_18new.png)
4. Select **DEPLOY** when the button gets highlighted.<br>
:warning: Wait until the deployment is completed.<br>
![assets/gitlabrunner_19new.png](assets/gitlabrunner_19new.png)

Now, you can enable cache for your GitLab CI jobs.<br>
For more information on how to enable the cache, see the [official GitLab documentation](https://docs.gitlab.com/ee/ci/yaml/#cache).

