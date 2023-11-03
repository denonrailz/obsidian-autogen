---
_id: 
version: "0.1"
type: knowledge
---
## Personas
This section describes the roles and responsibilities of personas that interact with the Anthos platform, and how and to what extent they interface with CloudApp Kubernetes Enterprise based on Google Anthos.
When considering Anthos, the following personas are important:  
![assets/responsibilities_1.png](https://docs.cloudapp.epam.com/assets/responsibilities_1.png)

> Please note that these personas represent job functions, not people.

## Application owners and developers
This group is responsible for developing and delivering applications and services to the end user. This group owns the application’s roadmap and the source code, including bug fixes, performance regressions, and incidents. Application developers need a platform to build, test, and reliably release software to their clients. Anthos platform admins (described in the following paragraph) ensure this functionality exists in the platform for the application owners.
These personas typically interface with Anthos through Git.

## Application administrators and operators (SRE/Ops)
This persona is responsible for operating live production deployments, monitoring their health, and rolling out updates as required. Their tier includes monitoring, capacity planning, deployment and rollouts, incident response, troubleshooting, automation, and scaling. They are ultimately responsible for maintaining the Service Level Objectives (SLOs) of a particular application or service. This group is responsible for designing and implementing CI/CD pipelines as well as monitoring systems to observe the performance and functionality of the application.
It is important to note that this group operates at the application service layer. Platform administrators are responsible for Anthos components and their management. They work with Google Cloud Support for Anthos-specific issues, whereas SRE/Ops work with both the application owners and platform administrators to ensure applications are kept within the required SLO.
These personas interface with Anthos through Git and CI/CD pipelines, Observability system, Google Cloud APIs or UI.

## Platform team
This group includes platform administrators, security, network, storage, and database administrators.
These personas are responsible for building and managing the life cycle of the Anthos platform itself. They continuously implement the capabilities of the Anthos platform, so that it is ready for use by the application owners. The platform team also consists of DevOps and software engineers who design, build, or set up various platform components (PaaS). They are not typically involved in daily platform operations. The platform team works on day-to-day aspects of the platform functionality to create scalable PaaS (IAM/security, Kubernetes and cluster management, PaaS creation, Observability components management, Policies management, and Network configuration).
## Detailed view

![assets/responsibilities_2.png](https://docs.cloudapp.epam.com/assets/responsibilities_2.png)