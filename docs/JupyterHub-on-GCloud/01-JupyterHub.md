
## Introduction

This document lays out the steps needed to setup a JupyterHub deployment on Google Cloud
using Kubernetes. All steps needed will be talked about in detail plus all the insight i’ve gained
through going through the process will be talked about for the benefit of the reader. Most of the
setup was accomplished by following the ​Zero to JupyterHub with Kubernetes​ guide.

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
last part, one can mostly follow the tutorial on the ​[website](https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-helm.html), where a lot of additional information
regarding Helm can be found too.

#### Notes:
<ul>
<li>The commands in the guide should be run on the Google Cloud Shell that was used in <br>
the last step.
<li>Closing or disconnecting from the console will remove helm ​, and one has to <br>
reinstall it again with <br>
curl https:​//​raw​.​githubusercontent​.​com​/​kubernetes​/​helm​/​master​/​scripts​/​get ​|​ bash <br>
to use helm commands to control the cluster.
</ul>

## Setting up JupyterHub

In this step, we setup JupyterHub on the Kubernetes cluster using Helm. One can mostly use
the ​[website](https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-jupyterhub.html#setup-jupyterhub)​.
#### Notes:
<ul>
<li>An example [configuration](https://github.com/LibreTexts/metalc/blob/master/docs/JupyterHub-on-GCloud/config-template.yaml) file is included in the folder fore reference.
<li>The commands in this tutorial should be run from the same Google Cloud Shell used in <br>
the last steps.
<li>Check that we can connect to JupyterHub in the browser.
<li>It is suggested to get a domain name at this point before proceeding to the next steps. <br>
There are options for free domain hosting websites like ​tk​(the option used for my setup, <br>
12 months of free hosting with no credit card requirement upfront).
</ul>

## Setting up OAuth

OAuth is very easy to setup for a Google Cloud Kubernetes setup. One can mostly follow the
tutorial on the ​[website](https://zero-to-jupyterhub.readthedocs.io/en/latest/authentication.html#google-oauth)
#### Notes:
<ul>
<li>Make sure to add the JupyterHub domain in the OAuth consent screen, under the <br>
‘Authorized Domains’.
<li>For step 10 on the website ​, we simply add that piece of code to the config.yaml file we <br>
setup in our previous steps.
</ul>

## Setting up HTTPS

One can mostly follow the guide on the ​[website](https://zero-to-jupyterhub.readthedocs.io/en/latest/security.html)​.
#### Notes:
<ul>
<li>Read the ‘Updating config.yaml’ section bellow.
<li>It might take a couple of minutes before HTTPS kicks in on JupyterHub, refresh if not <br>
working yet.
</ul>

## Customizing User Environments

The ​[website](https://zero-to-jupyterhub.readthedocs.io/en/latest/user-environment.html)​ is the place to look at for available customizations.
#### Notes:
<ul>
<li>Near the bottom of this [page](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/running.html#using-binder) there seems to be the possibility of running a user server <br>
with binder? Needs more research to confirm this.
<li>The main way used for JupyterHub to customize a user environment is the use of <br>
Docker images for building user servers when someone logs in. At the bottom of the <br>
website, it is explained how JupyterHub can be setup to give the user a choice of <br>
environment to use when starting their server.
<li>Users can use the new JupyterLab interface by changing the ​ **/tree** ​ part of the <br>
JupyterHub url to ​ **/lab** ​. It is also possible to make JupyterLab the default interface for <br>
when a user logs in.
</ul>

## Updating config.yaml(Read before changing config.yaml)

Most of the configurations for the cluster are made in the config.yaml file that we created in the
the previous steps. ​[Zero to JupyterHub with Kubernetes​](https://zero-to-jupyterhub.readthedocs.io/en/latest/index.html) contains a lot of documentation on all
kinds of possible configurations for a cluster. ​ **Important: when indenting in the config.yaml
file, don’t use tabs, always use two spaces.**

### Potential Errors:
<ul>
<li>If helm is missing, run:
curl https:​//​raw​.​githubusercontent​.​com​/​kubernetes​/​helm​/​master​/​scripts​/​get ​|​ bash
<li>If ‘client versions don’t match’, run: helm init --upgrade
</ul>

### Steps for updating config.yaml:

1. After changing the config.yaml file we need to update the cluster with a helm command.
2. Run: RELEASE=jhub in the cloud shell. (This step is only needed if the shell was
    restarted after the initial setup)
3. Run: helm upgrade $RELEASE jupyterhub/jupyterhub --version=0.8.0 --values
    config.yaml
4. Wait for the command to finish, this might take a couple of minutes.

5. Run: kubectl get pod --namespace jhub (​ **this is assuming we are using the jhub**
    **namespcae, the one used in the tutorial** ​)
6. Wait for all the pods to be in the ‘RUNNING’ status before checking JupyterHub in the
    browser for the changes.
7. Done!
