# Docs

This directory contains all relevant or useful documentation pertaining to the set-up and maintenance 
of a Kubernetes cluster for the purpose of hosting Jupyter/Binder hub deployments, among other things. 

## Table of Contents

### Bare-Metal
The Bare-Metal directory contains leftover information from the flock cluster that could still be 
considered relevant.

1. [login.md](Bare-Metal/login.md) Contains the text on the login page for the Jupyterhub deployment verbatim.
1. [ZFS.md](Bare-Metal/ZFS.md) Contains information pertaining to the ZFS server set up for persistent storage 
for the cluster.

#### Concepts
[Bare-Metal/concepts/](Bare-Metal/concepts/) contains documents detailing various topics related to the cluster.

#### Troubleshooting
[Bare-Metal/troubleshooting/](Bare-Metal/troubleshooting/) documents troubleshooting problems and solutions. Readers should consult this section 
when dealing with an issue.

### Virtual Machine
1. [JupyterHubVM.md](Virtual-Machine/JupyterHubVM.md) gives instructions on setting up JupyterHub on a
virtual machine with RAID1 using the LibreTexts fork of the [jupyter-deploy-teaching](https://github.com/LibreTexts/jupyterhub-deploy-teaching/) repository. [More information on RAID](./docs/Bare-Metal/concepts/RAID.md) could 
be found in the concepts section.
1. [baremetal_jhub.md](Virtual-Machine/baremetal_jhub.md) is Kevin's (@kkrausse) instructions for
setting up JupyterHub on a virtual machine. It contains solutions to the problems we faced
when installing JupyterHub through the [jupyterhub-deploy-teaching](https://github.com/mechmotum/jupyterhub-deploy-teaching)
repository. We keep this as a reference for those who might encounter the same problems in the future.

### JupyterHub on GCloud
This section teaches how to set-up and configure JupyterHub on Google Cloud.

1. [01-JupyterHub.md](JupyterHub-on-GCloud/01-JupyterHub.md) describes how to set up Kubernetes, Helm, 
and JupyterHub on Google Cloud. It also describes how to configure OAuth, HTTPS, and user environments.
1. [02-AddingKernelsToJupyter.md](JupyterHub-on-GCloud/02-AddingKernelsToJupyter.md) describes how to
install the R and Octave kernels in JupyterHub. 
1. [03-LoadBalancer.md](JupyterHub-on-GCloud/03-LoadBalancer.md) describes the purpose of a load
balancer and the process of setting it up on Google Cloud.

### BinderHub on GCloud
1. [01-BinderHub.md](Binder-on-GCloud/01-BinderHub.md) gives instructions on setting up BinderHub
on a Kubernetes cluster on Google Cloud.

### Galaxy-Control-Repo.md
This document gives a general overview of setting up the current galaxy cluster.

### maintenance-tasks.md
Outlines general maintenance tasks that need to be performed regularly.

### Onboarding.md
This file helps onboard new hires into the Jupyter team.