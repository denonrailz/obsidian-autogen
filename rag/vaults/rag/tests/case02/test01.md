---
_id: 
question: How to deploy gitlab runners? Do I need to to use it in same cluster or in external and how to provide them permissions?
version: "0.1"
type:
  - q&a
---
To deploy GitLab Runners, you can use the Kubernetes executor and run CI/CD jobs in your Kubernetes cluster. You can deploy the runners in the same cluster or in an external cluster. To provide permissions, you can use the "overwrite" functionality to enable cluster-wide access and create a Kubernetes service account with the required role bindings. For more details on how to deploy GitLab Runners and provide permissions, you can refer to the official GitLab documentation: [GitLab Runner installation](https://docs.gitlab.com/runner/install/kubernetes.html) and [Overwrite the Kubernetes namespace](https://docs.gitlab.com/runner/executors/kubernetes.html#overwrite-the-kubernetes-namespace).
