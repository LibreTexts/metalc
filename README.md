# Metal Cluster

This is our repo for everything involving our bare-metal Kubernetes cluster. At this moment, 
it also contains documentation for setting up Kubernetes, JupyterHub, and BinderHub on Google Cloud. 
The folder [docs](./docs) contains all documentation related to these topics. 
The root of this repository contains files relating to the set-up of the bare-metal cluster, 

## Table of Contents
This discusses the table of contents of [documentation](./docs) folder based on the following topics.

### Bare-Metal
1. [Bare Metal Cluster Setup](./docs/Bare-Metal/baremetal.md) has what you should read first about
  the cluster. The file gives an overview of the cluster set-up, including networking, publishing services,
  instructions on adding nodes, and useful resources.

#### Concepts
1. [RAID.md](./docs/Bare-Metal/concepts/RAID.md) describes the purpose and different levels of RAID.

#### Troubleshooting
This section documents troubleshooting problems and solutions. Readers should consult this section 
when dealing with an issue.

1. [Adding Not Ready Node](./docs/Bare-Metal/troubleshooting/AddingNotReadyNode.md) troubleshoots adding a node
in a NotReady state, with error code 255. The process works best for adding a node that is considered
to be part of the cluster.
1. [Deleted Kube DNS Service](./docs/Bare-Metal/troubleshooting/DeletedKubeDNSService.md) troubleshoots
accidentally deleting and readding a service from the cluster. In this case, the `kube-dns` service is deleted;
this could be useful for other services that may be deleted.

### Virtual Machine
1. [JupyterHubVM.md](./docs/Virtual-Machine/JupyterHubVM.md) gives instructions on setting up JupyterHub on a
virtual machine with RAID1 using the LibreTexts fork of the [jupyter-deploy-teaching](https://github.com/LibreTexts/jupyterhub-deploy-teaching/) repository. [More information on RAID](./docs/Bare-Metal/concepts/RAID.md) could 
be found in the concepts section.
1. [baremetal_jhub.md](./docs/Virtual-Machine/baremetal_jhub.md) is Kevin's (@kkrausse) instructions for
setting up JupyterHub on a virtual machine. It contains solutions to the problems we faced
when installing JupyterHub through the [jupyterhub-deploy-teaching](https://github.com/mechmotum/jupyterhub-deploy-teaching)
repository. We keep this as a reference for those who might encounter the same problems in the future.



### JupyterHub on GCloud
This section teaches how to set-up and configure JupyterHub on Google Cloud.

1. [01-JupyterHub.md](./docs/JupyterHub-on-GCloud/01-JupyterHub.md) describes how to set up Kubernetes, Helm, 
and JupyterHub on Google Cloud. It also describes how to configure OAuth, HTTPS, and user environments.
1. [02-AddingKernelsToJupyter.md](./docs/JupyterHub-on-GCloud/02-AddingKernelsToJupyter.md) describes how to
install the R and Octave kernels in JupyterHub. 
1. [03-LoadBalancer.md](./docs/JupyterHub-on-GCloud/03-LoadBalancer.md) describes the purpose of a load
balancer and the process of setting it up on Google Cloud.

### BinderHub on GCloud
1. [01-BinderHub.md](./docs/Binder-on-GCloud/01-BinderHub.md) gives instructions on setting up BinderHub
on a Kubernetes cluster on Google Cloud.

### Test Kubernetes Environment

We created a development [cluster of vms](./dev-env) using Vagrant that is nice
for testing stuff without having it on the main cluster. This section contains files 
and instructions implementing the test cluster.


