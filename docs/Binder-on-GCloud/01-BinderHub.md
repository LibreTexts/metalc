## Introduction

This document lays out the steps needed to setup a BinderHub deployment on Google Cloud
using Kubernetes. All steps needed will be talked about in detail plus all insight i’ve gained
through going through the process will be talked about for the benefit of the reader. Most of the
setup was accomplished by following the ​Zero to BinderHub guide.

## Setting up Kubernetes on Google Cloud

One can mostly follow the tutorial on the [​website​](https://zero-to-jupyterhub.readthedocs.io/en/latest/google/step-zero-gcp.html).

#### Notes:
<ul>
<li>On step 7, creating a node pool for users. The command won’t run unless either --region <br>
or --zone option was specified. I chose --region us-central1-b, the region that I used was <br>
the same one used in step 4 in the Kubernetes guide.
</ul>

## Setting up Helm

Helm​, the package manager for Kubernetes, is a useful tool for: installing, upgrading and
managing applications on a Kubernetes cluster. Helm packages are called ​ charts ​. Like for the
last part, one can mostly follow the tutorial on the ​[website](https://binderhub.readthedocs.io/en/latest/create-cloud-resources.html), where a lot of additional information
regarding Helm can be found too.

#### Notes:
<ul>
<li>The commands in the guide should be run on the Google Cloud Shell that was used in <br>
the last step.
<li>Closing or disconnecting from the console will remove helm ​, and one has to <br>
reinstall it again with <br>
'curl https:​//​raw​.​githubusercontent​.​com​/​kubernetes​/​helm​/​master​/​scripts​/​get ​|​ bash' <br>
to use helm commands to control the cluster.
</ul>

## Setting up a Container Registry

BinderHub builds Docker images out of Git repositories, and then pushes them to a Docker
registry so that JupyterHub can launch user servers based on these images. There are several
options available to use as a container registry, the one that will be used for this tutorial
is DockerHub. One can follow the tutorial for DockerHub on the [website](https://binderhub.readthedocs.io/en/latest/setup-registry.html). It also seems possible to run your own server as a Container Registry.

## Setting up BinderHub

In this step, we setup BinderHub on the Kubernetes cluster using Helm. One can mostly use
the ​[website](https://binderhub.readthedocs.io/en/latest/setup-binderhub.html)​.

#### Notes:
<ul>
<li>At the '1.2.2 Initialization' section, the command at step 2 has to be run in order for <br>
steps further in the installation to work.
</ul>

## Setting up Authentication

In this setp, we setup BinderHub Authentication following the steps on this [website](https://binderhub.readthedocs.io/en/latest/authentication.html). This step is only useful if 
we want to redirect our users to a login page when they arrive at our BinderHub URL. Usually we will
not need a login page (mybinder.org does not have a login page).

#### Notes:
- Binder Oauth requires a binderhub domain and a jupyterhub domain. 

## JupyterHub Customization

In this step, we can customize [JupyterHub user resource](https://zero-to-jupyterhub.readthedocs.io/en/latest/user-resources.html) and other customization by editing config.yaml. 
This [page](https://binderhub.readthedocs.io/en/latest/customizing.html) provides a general 
jupyterHub customization description, but the format it provides is incorrect. See the config-template.yaml
file provided. More explanations can be found on [page1](https://binderhub.readthedocs.io/en/latest/debug.html) 
and [page2](https://discourse.jupyter.org/t/nesting-levels-in-config-yml-file/1037)


## Q&A
Get more help about Binderhub on [discourse](https://discourse.jupyter.org) and [GitHub issue](https://github.com/jupyterhub/binderhub) and [mybinder github](https://github.com/jupyterhub/mybinder.org-deploy)
