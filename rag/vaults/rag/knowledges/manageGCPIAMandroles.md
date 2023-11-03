---
_id: 
version: "0.1"
type: knowledge
---
# Managing GCP IAM and roles

## Introduction
The main purpose of this documentation is to address the following questions:

- What default permissions are granted to users for access to the project?
- How can a user independently manage access rights to the project (assign and restrict)?
- To whom can a user grant access rights?

When creating a new Anthos Fleet, which includes a GCP Project with pre-configured GKE Enterprise Kubernetes clusters, an Application Team Admin group is automatically generated, and IAM roles for this group are set up. This is done to provide end-users (Application teams) access to the necessary services for working with GKE clusters. It simplifies the onboarding process with GKE clusters and grants a fundamental set of essential Google services. Nevertheless, project administrators within the Application teams can also utilize the Self-service feature to independently assign additional roles to themselves or other team members.

Below, you'll find all the necessary information and details on these topics, organized into the following sections:

- **IAM Defaults**. This section outlines the default configurations and how to get started when logging in for the first time.
- **IAM Self-service**. In this section, you'll discover additional capabilities for role assignment and how to request extended permissions through the Support Portal, which may not be available by default according to company policies.

## IAM Defaults
- Upon activating each Anthos Fleet, a **Special< EPAM_PROJECT_CODE >GCP-Operations@epam.com** group is provided for administrators of the GCP project within the Application team. This group is created in EPAM AD and is pre-populated with members, including the project manager and the project's application team members. You can add new users to this distribution list (DL) who have extended permissions by raising a [request](https://support.epam.com/ess?id=sc_cat_item&sys_id=abc4914a974ed590386e3a871153aff4) at Support Portal. Note, that project manager approval will be required during the process. You can find the preinstalled roles in Google Console as described [here](https://kb.epam.com/display/EPMPAAS/Manage+GCP+IAM+and+roles_reviewed#ManageGCPIAMandroles_reviewed-HowtoviewdefaultrolesforDLsofclientadministrators).
- More detailed instructions for populating DLs for client project administrators can be found in the EPAM Cloud documentation by the following [link](https://kb.epam.com/display/public/EPMCITFAQ/Setting+up+permissions+in+GCP+projects+within+EPAM+Cloud+Service).

![/assets/gcpiamrules.png](/assets/gcpiamrules.png)

### How to view default roles for DLs of client administrators
1. In GCP Console, navigate **IAM & Admin → IAM**.
2. Select your DL (**Special< EPAM_PROJECT_CODE >GCP-Operations@epam.com**) and view default roles.<br>
![/assets/manageGCPIAM_2.png](/assets/manageGCPIAM_2.png)

## IAM Self-service
You, as an application team member, can independently assign roles from the list of available ones. For assigning other roles, not available for self-service according to EPAM Policies, you can use the Support Portal.
- By default, only the group **Special< EPAM_PROJECT_CODE >GCP-Operations@epam.com** has access to the project.
- You can find information on how to manage the group of project administrators (**Special< EPAM_PROJECT_CODE >GCP-Operations@epam.com**), which is included by default in the project, in this [document](https://kb.epam.com/pages/releaseview.action?spaceKey=EPMCITFAQ&title=Setting+up+permissions+in+GCP+projects+within+EPAM+Cloud+Service).
- The default roles assigned to this group can be viewed in Google Console as described [here](https://kb.epam.com/display/EPMPAAS/Manage+GCP+IAM+and+roles_reviewed#ManageGCPIAMandroles_reviewed-HowtoviewdefaultrolesforDLsofclientadministrators).
- If the project requires an additional DL with a different set of roles, you can request the creation of a new DL via the [Support Portal](https://support.epam.com/ess?id=sc_cat_item_guide&sys_id=fd616d9c476f5958ed13b2bd436d43d4&name=Email,Mailboxes,AndDistributionGroups). Afterward, you need to request the synchronization of the created DL with Google on the Support Portal. Once the synchronization is configured, administrators can assign the necessary roles to this DL.
- Additionally, by default, administrators of the DL have the right to assign roles to particular users (IAM users) who are synchronized with Google by default and do not require additional synchronization configuration.
- Administrators of the DL can also create [Google groups](https://groups.google.com/), populate them with users, and assign roles to them within the scope of their project. In this case, the management of these groups remains with the project and the project's administrative group.
- The addition of new users/DL is carried out independently by users from the **Special< EPAM_PROJECT_CODE >GCP-Operations@epam.com** group by assigning roles in the IAM section to users from the allowed list of roles for IAM Self-service. You can view the list by clicking **allowed roles**.
![/assets/manageGCPIAM_3.png](/assets/manageGCPIAM_3.png)
- Assigning roles that are **not included** in the list of allowed roles can be [requested](https://support.epam.com/ess?id=sc_cat_item_guide&sys_id=5ec240da973ba114386e3a871153af7a&name=CloudAccessManagement) through Support Portal.
- Periodically, EPAM Cloud automation runs to verify whether users correspond to an EPAM project that owns a Google account (project). If users don't belong to an EPAM project, they will be automatically removed, along with their Google project. If such users are part of a DL, they will also be removed. To be added on a permanent basis, you need to discuss a full project assignment with the project or delivery manager. You can be added by a project member, too.

### How to add a role to a user/group
1. Navigate **IAM & Admin → IAM → Grant access**.<br>
![/assets/manageGCPIAM_4.png](/assets/manageGCPIAM_4.png)
2. Specify the principal user/DL/group, select a role, and click **Save**.<br>
![/assets/manageGCPIAM_5.png](/assets/manageGCPIAM_5.png)

- If the project needs to differentiate permissions within GKE clusters, it is recommended to use the Google Anthos Teams service. Please note that this service currently **does not support working with DLs**. To control permissions, you can only use specific IAM users or Google Groups. For more information, you can refer to the [Namespaces RBAC Management](https://kb.epam.com/display/EPMPAAS/Namespaces+RBAC+Management) document.
