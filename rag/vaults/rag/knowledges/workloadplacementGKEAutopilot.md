---
_id: 
version: "0.1"
type: knowledge
---
# Workload placement - GKE Autopilot

## Overview
Google Kubernetes Engine (GKE) Autopilot is Google's managed Kubernetes solution. Compared to GKE Standard, Google handles the management of nodes and node groups, and you, as a Client, are not billed for unused resources. For more in-depth information on how GKE Autopilot differs from GKE Standard, see the official documentation: [Autopilot overview](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview) and [Autopilot and Standard feature comparison](https://cloud.google.com/kubernetes-engine/docs/resources/autopilot-standard-feature-comparison#feature-comparison).

To learn more about GKE Autopilot, see the following how-to guides:<br>
- [Deploy workloads on GKE Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview#deploy-workloads)<br>
- [Use predefined compute classes in Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-compute-classes)<br>
- [Specify zone for pods](https://cloud.google.com/kubernetes-engine/docs/how-to/gke-zonal-topology)<br>
- [Specify nodes for pod](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-separation)<br>
- [Use spot instances for pods](https://cloud.google.com/kubernetes-engine/docs/how-to/autopilot-spot-pods)<br>
- [Use affinity and anti-affinity](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview#pod_affinity_and_anti-affinity)<br>
- [Extend the run time of Autopilot pods](https://cloud.google.com/kubernetes-engine/docs/how-to/extended-duration-pods)

### Examples
To learn how to effectively use workload placement, review the following examples:

#### Selecting compute class to run pod
This option allows choosing a node type on which the exact pod will be run.<br>

| Compute class | Description |
| ----------- | ----------- |
| General-purpose | Default class; used if a specific compute class is not defined. |
| Balanced | Used to request more CPU or memory than [the default class](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-resource-requests#min-max-requests) allows or to select specific CPU architecture. |
| Scale-Out | Used to utilize single thread-per-core computing and horizontal scaling (1 vCPU is equivalent to the entire core). |

##### Specifying compute class and cpu architecture using node selector
```
spec:
  replicas: 2
  template:
    spec:
      containers:
        - ...
      nodeSelector:
        cloud.google.com/compute-class: "Balanced"
        kubernetes.io/arch: "arm64"
```
##### Specifying compute class using node affinity
```
spec:
  replicas: 2
  template:
    spec:
      containers:
        - ...
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: cloud.google.com/compute-class
                    operator: In
                    values:
                      - "Scale-Out"
```
#### Placing workload to specific zone

##### Specifying zone A using node selector
```
spec:
  replicas: 2
  template:
    spec:
      containers:
        - ...
      nodeSelector:
        topology.kubernetes.io/zone: "europe-west3-a"
```

##### Specifying zones A and B using node affinity
```
spec:
  replicas: 2
  template:
    spec:
      containers:
        - ...
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: topology.kubernetes.io/zone
                    operator: In
                    values:
                      - "europe-west3-a"
                      - "europe-west3-b"
```

#### Placing workload to spot instance

##### Scheduling workload on spot instance in zone A using node selector
```
spec:
  replicas: 2
  template:
    spec:
      containers:
        - ...
      terminationGracePeriodSeconds: 25
      nodeSelector:
        topology.kubernetes.io/zone: "europe-west3-a"
        cloud.google.com/gke-spot: "true"
```

##### Scheduling workload on spot instance in zone A and B using node affinity
```
spec:
  replicas: 2
  template:
    spec:
      containers:
        - ...
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: topology.kubernetes.io/zone
                    operator: In
                    values:
                      - "europe-west3-a"
                      - "europe-west3-b"
              - matchExpressions:
                  - key: cloud.google.com/gke-spot
                    operator: In
                    values:
                      - "true"
```

#### Using pod affinity and anti-affinity

##### Using anti-affinity to run pods on different nodes
```
spec:
  replicas: 2
  template:
    spec:
      containers:
        - ...
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - myapp
              topologyKey: kubernetes.io/hostname
```

#####  Using affinity to run pods on the same node
```
spec:
  replicas: 2
  template:
    spec:
      containers:
        - ...
      affinity:
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - myapp
              topologyKey: topology.kubernetes.io/zone
```

#### Using dedicated node group to run pods

##### Scheduling workload on spot instance in zone A using node selector
```
spec:
  replicas: 2
  template:
    spec:
      containers:
        - ...
      tolerations:
        - key: group
          operator: Equal
          value: "restricted"
          effect: NoSchedule
      nodeSelector:
        group: "restricted"
```

#### Prolonging pod lifetime

##### Using annotation to prolong pod lifetime
```
spec:
  replicas: 2
  template:
    metadata:
      annotations:
        cluster-autoscaler.kubernetes.io/safe-to-evict: "false"
    spec:
      containers:
        - ...
```
