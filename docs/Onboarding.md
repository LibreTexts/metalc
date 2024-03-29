# Onboarding

This file helps onboard new hires into the Jupyter team. We currently maintain
[jupyter.libretexts.org](https://jupyter.libretexts.org), a JupyterHub for
LibreTexts and UC Davis users.

# HR

Your immediate supervisors are:

- Richard Feltstykket

You can reach out to them about any issues you need to discuss. If you don't
feel comfortable reaching out to them (like if you need to report something
about them) you can reach out to their supervisors. Richard's is Matt Settles.

You will be hired under the Chemistry Department and paid through LibreTexts
related funds. You can contact Hongfei Wang <hfwwang@ucdavis.edu> about any 
HR issues (getting paid, trs hour submission, etc.). Delmar Larsen
<dlarsen@ucdavis.edu> runs the LibreTexts project and you can contact him about
any high level issues with the project or Department of Education grant.

## Getting Started

### Overview
- [ ] [Generate an SSH public key](https://confluence.atlassian.com/bitbucketserver/creating-ssh-keys-776639788.html) if you haven't already, or use [PuTTYGen](https://www.ssh.com/ssh/putty/windows/puttygen) if you want to use PuTTY.
- [ ] Ask for your public key to be added to Gravity, the LibreTexts test server at query.libretexts.org, and the galaxy control repo.
- [ ] Ask for your email account to be added as an Admin on jupyter.libretexts.org and staging.jupyter.libretexts.org
- [ ] Be added to:
  - [ ] jupyterteam mailing list: https://lists.ucdavis.edu/sympa/info/jupyterteam
  - [ ] Discord (we also have a Slack, not in current use)
  - [ ] Google Drive
  - [ ] Jupyter-team GitHub team: https://github.com/orgs/LibreTexts/teams/jupyter-team
  - [ ] Private configuration repo and galaxy control repo
  - [ ] Libretexts-Jupyter Forum: https://libretexts-constructionforum.groups.io/g/jupyter/
- [ ] Claim your server room key card, if on campus

### Connecting to Gravity

The cluster is under a private network, so the only way to access the cluster
is by SSHing into Gravity, our management server.

If you have Windows, it would probably be easier to 
install [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
PuTTY makes it easier for you to SSH into gravity. Otherwise, you can
use the command line. For Windows, another very good alternative to using PuTTY, is installing a [WSL](https://www.windowscentral.com/install-windows-subsystem-linux-windows-10). It lets you run Linux alongside Windows without the need to install a virtual machine.

You need to give your public key to someone who currently has access
to gravity so that you can SSH into the server. 
[Generate your SSH key](https://confluence.atlassian.com/bitbucketserver/creating-ssh-keys-776639788.html)
if you haven't already. If you are using PuTTY, generate your SSH key
using [PuTTYGen](https://www.ssh.com/ssh/putty/windows/puttygen). 

Afterwards, email your public key (should be the file `id_rsa.pub`
or something similar) to someone who has access to gravity. **Do not
email your private key.**

Ask us in person for the username and password.

(For those with access to the server) 
To add the key into gravity, follow these steps:
  1. ssh into the server using ssh gravity
  2. cd ~/.ssh
  3. nano authorized_keys
  4. Scroll to the bottom of the nano file and paste your key in
  5. Save the file using Ctrl + O

### Joining Our Communication Channels

We use Discord and Google Chat to communicate. Make sure that you get invited to
both of these channels.

Discord is mainly used by students, while Google is mainly used by your supervisors.

We also have a shared Google Drive (which is pretty inactive) containing
past presentations and general overviews of the cluster.

### Exchange Phone Numbers and Emails

If you haven't already, please request to add yourself to the 
mailing list: jupyterteam@ucdavis.edu. All emails sent to this address
will be sent to you. This email address is a support email for LibreTexts
and UC Davis users if they encounter any problems with JupyterHub and 
a way for all associated employees to communicate with each other.

[This Google document](https://docs.google.com/document/d/1dXeBmY8jEpVsvfAfu4JYSyvXageEi2URO9XS-0bdsHY/edit#)
has everyone's contact information; feel free to add yours.

### AIOs

AIO stands for "Accomplishments, Issues, and Objectives." The concept
comes from former supervisor Jason Moore's lab. Weekly AIO emails are to be sent to keep track of progress and objectives.
More info about AIO's can be found [here](https://mechmotum.github.io/guide.html#aio-weekly-emails).

## Logging Your Hours

Once you get hired, you will log your hours on
[trs.ucdavis.edu](https://trs.ucdavis.edu). You should also
receive a key card which can get you access to the server room. Matt Settles
can give you key card access.

## Working on GitHub

We document our work on GitHub. This is so that any current or future workers
can refer back to the work already done.

There are a couple of repositories we use:
* [metalc](https://github.com/LibreTexts/metalc/) is the main repository for issue tracking.
There are also many miscellaneous documents of varied relevance scattered throughout the repo.
Unless an issue is very specific to another repository, it should be posted here.
* [default-env](https://github.com/LibreTexts/default-env) contains files used to create the Default Environment in Jupyter. 
This can be used with repo2docker to generate our default user 
image for everyone using our JupyterHub and code cells on the LibreTexts website.
* [ckeditor-binder-plugin](https://github.com/LibreTexts/ckeditor-binder-plugin) is a plugin which lets
LibreTexts authors add executable code blocks into the LibreTexts text editor. LibreTexts uses CKEditor.
for its text editor; thus our plugin uses the CKEditor API. It uses 
[BinderHub](https://binderhub.readthedocs.io/en/latest/) in the backend to execute these code blocks.
* [protogalaxy](https://github.com/LibreTexts/protogalaxy) is a Puppet module we use to spin up a highly available Kubernetes cluster.
* [widget-testing](https://github.com/LibreTexts/widget-testing) tracks inconsistencies with ipywidgets in [ckeditor-binder-plugin](https://github.com/LibreTexts/ckeditor-binder-plugin) code blocks between [Thebe](https://github.com/executablebooks/thebe), JupyterHub, and LibreTexts.

We also have two important private repositories:
* metalc-configurations contains all Kubernetes config files for Flock, various service configurations for rooster, documentation on the hardware/networking of the cluster, and credentials.
* galaxy-control-repo contains the puppet code that applies to every node in the Galaxy cluster, as well as all Kubernetes objects on Galaxy.

Some less frequently updated or slightly out of scope repositories:
* [mechmotum.github.io](https://github.com/LibreTexts/mechmotum.github.io) is our fork 
of Jason's website. We write blog posts on this fork and later make pull requests to 
merge on his repository.
* [jupyterhub-templates](https://github.com/LibreTexts/jupyterhub-templates) 
contains custom HTML pages for the website (the login page, about page and FAQ page). Updating these on GitHub will
update the website if JupyterHub gets upgraded.
* [executablebooks/thebe](https://github.com/executablebooks/thebe) allows code blocks in HTML pages transform into live, executable code blocks. Thebe is used by the [ckeditor-binder-plugin](https://github.com/LibreTexts/ckeditor-binder-plugin).
* [ckeditor-query-plugin](https://github.com/LibreTexts/ckeditor-query-plugin) is a tool we use on the LibreTexts website to embed HTML in textbooks.
* [ngshare](https://github.com/LibreTexts/ngshare) allows nbgrader to be used in a Kubernetes JupyterHub. We have this installed in our JupyterHub, and future instructors may use this.


We track our current tasks on [Issues](https://github.com/LibreTexts/metalc/issues).
Feel free to assign yourself to an issue! It is recommended that you start with the issues labelled as "good first issue". They will probably be a little less technical and easier to deal with.

## Working With the Cluster

### Galaxy cluster

Our cluster setup is named Galaxy. It currently has 8 nodes: one management node (gravity), five control-plane (master) nodes (nebula1-nebula5) and 12 (functional) worker nodes (star2-star13). The network diagram for this is available in metalc-configurations.

### Networking

You should have a decent understanding of computer networks (if you don't, please do not hesitate asking your peers! Networking is not easy, so it never hurts to get some extra help). Try to make sure you understand what these terms mean: layer 2 (also ARP, MAC addresses), layer 3 (also IP addresses, subnets, CIDR notation), DHCP, routers vs switches, VLAN, layer 4 (TCP), DNS, HTTP/HTTPS, linux network interfaces (using the `ip` command).

(Don't worry if you don't understand these! You will get used to them once you work with our networking setups a bit more. Sorry for dumping a bunch of terms on you. You don't need to know everything coming in, and you can take a couple of months learning things gradually.)

To get a full understanding of our network setup, read the networking info documentation in metalc-configurations, the [HA setup used in protogalaxy](https://github.com/LibreTexts/protogalaxy#architecture), and some of the multus configurations in our control repo. You can just read the networking info document to get started, and read the rest later.

### Containers
A container is like a really lightweight virtual machine (it is not quite a VM). It packages up an application and all of its dependencies, so you get a reproducible image that you can run anywhere.

You should understand two concepts: images and containers. Some reading material: [What is a container](https://www.docker.com/resources/what-container), and [how to get started](https://docs.docker.com/get-started/).

Containers are the building blocks of Kubernetes and all of our services in the cluster, so you will be dealing with them quite a bit. I recommend installing Docker in your Linux or WSL environment, so you can develop / test things locally.

### Kubernetes
Kubernetes is a way to run containers across multiple physical machines (nodes), among other things. You can create things like deployments in Kubernetes, and it will automatically schedule containers on your nodes. If a container dies for some reason, it will reschedule the container so your service stays up.

We recommend reading some of the following:
* [Introduction to Kubernetes](https://www.digitalocean.com/community/tutorials/an-introduction-to-kubernetes)
by Digital Ocean gives a good overview of what Kubernetes is and its basic concepts.
* [Play with Kubernetes](https://labs.play-with-k8s.com/) lets you test out building Kubernetes
clusters online!
* [What even is a kubelet](http://kamalmarhubi.com/blog/2015/08/27/what-even-is-a-kubelet/) is a bit
more of a technical introduction to Kubernetes.
* [Kubernetes Documentation](https://kubernetes.io/docs/concepts/) is an in-depth look at
Kubernetes. It's a technical, complete documentation of the software. This could or
could not serve as a good introduction to Kubernetes, depending on the person.

### Helm
We use Helm to "install" things into our Kubernetes cluster. You can think of Helm as a tool that takes in a recipe (called a Helm chart), some configuration values (Helm values), and generates a bunch of Kubernetes objects to be deployed into our cluster (such as Deployments, PVCs, ConfigMaps, Services, etc). It's an easy way to deploy an application into Kubernetes. We use Helm to install JupyterHub, BinderHub, the Prometheus-Grafana stack, among other things. The Helm values we use are available in the private configuration repos, and a list of all the Helm charts we install are in the cluster-info document in metalc-configurations.

### JupyterHub
**JupyterHub** is a service that allows multiple users to create notebooks with code.

[Zero to JupyterHub with Kubernetes](https://zero-to-jupyterhub.readthedocs.io/en/latest/)
is the main documentation for building a JupyterHub cluster from Kubernetes.
You can try to build your own on Google Cloud, but this will cost money
(*unless*: if you have not used Google Cloud before, you can get $300 free credits).

If you want to know more about what Jupyter is, visit [https://try.jupyter.org](try.jupyter.org).

### Grafana
Our alerting and monitoring system is based on Prometheus, with Grafana dashboard powering the front end. You can access the dashboards and in grafana.libretexts.org. To change these dashboards, follow the documentation in our private configuration repos.

### Quick Guide to Navigating Kubernetes
`kubectl` is the main way for us to get information from Kubernetes via the command line.
After you SSH into gravity, try out a few of the following `kubectl` commands:

1.  `kubectl get nodes`
```
NAME      STATUS   ROLES                  AGE   VERSION
nebula1   Ready    control-plane,master   9d    v1.20.1
nebula2   Ready    control-plane,master   9d    v1.20.1
nebula3   Ready    control-plane,master   9d    v1.20.1
nebula4   Ready    control-plane,master   9d    v1.20.1
nebula5   Ready    control-plane,master   9d    v1.20.1
star10    Ready    <none>                 9d    v1.20.1
star11    Ready    <none>                 9d    v1.20.1
star12    Ready    <none>                 9d    v1.20.1
star13    Ready    <none>                 9d    v1.20.1
star2     Ready    <none>                 9d    v1.20.1
star3     Ready    <none>                 9d    v1.20.1
star4     Ready    <none>                 9d    v1.20.1
star5     Ready    <none>                 9d    v1.20.1
star6     Ready    <none>                 9d    v1.20.1
star7     Ready    <none>                 9d    v1.20.1
star8     Ready    <none>                 9d    v1.20.1
star9     Ready    <none>                 9d    v1.20.1
```

  This shows all of the nodes on the cluster. You can see the status of each.

2. `kubectl get pods -A`
   ```
   NAMESPACE        NAME                                                        READY   STATUS        RESTARTS   AGE
   binderhub        autohttps-59dd446c76-59mbn                                  2/2     Running       0          52d
   binderhub        binder-5696db87dc-2qll2                                     1/1     Running       0          26d
   binderhub        binderhub-image-cleaner-2qlsm                               1/1     Running       0          8d
   ...
   ```
   This outputs all of the pods currently on the cluster.
  
3. `kubectl get pods -n jhub`
   ```
   NAME                                 READY   STATUS    RESTARTS   AGE
   autohttps-7b4fb9dd6b-gb6td           2/2     Running   0          25d
   continuous-image-puller-7h4jr        1/1     Running   0          32h
   continuous-image-puller-7mv45        1/1     Running   0          32h
   ...
   ```
   This outputs all the pods in the `jhub` namespace. The `jhub` namespace contains
   pods related to our JupyterHub instance.
  
4. Now try logging into JupyterHub and spawn a server. Run `kubectl get pods -n jhub` again.
   You should see a new pod with the name `jupyter-<your email>`.
   ```
   NAME                                            READY   STATUS    RESTARTS   AGE
   ...
   jupyter-<username of email>-40ucdavis-2eedu     1/1     Running   0          1m
   ...
   ```
  
5. `kubectl describe pod hub-<fill in random string you get from kubectl get pods here> -n jhub`
   ```
   Name:               hub-84595b4df9-2tn6h
   Namespace:          jhub
   Priority:           0
   PriorityClassName:  <none>
   ...
   ```
   This gives a description of the pod, including which node the pod is running on, its tolerations,
   etc. Sometimes, it will show some logs at the bottom. Note that this command will fail if you 
   don't include `-n jhub` in the command; Kubernetes usually requires for you to specify a
   namespace if its not in the default one.
   
6. `kubectl exec hub-<fill in random string you get from kubectl get pods here> -n jhub -ti bash`
   ```
   jovyan@hub-<random string>:/srv/jupyterhub$
   ```
   This lets you enter the pod and use its command line. You can explore the directories here
   to see what kind of files are used. This pod is almost like running the original 
   [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/) without knowledge of Kubernetes.
   Type `exit` to exit the pod.
  
7. `kubectl logs hub-<fill in random string you get from kubectl get pods here> -n jhub`
   ```
   ...
   [I 2019-10-13 19:26:56.957 JupyterHub log:174] 200 GET /hub/health (@10.0.0.113) 1.57ms
   [I 2019-10-13 19:27:06.957 JupyterHub log:174] 200 GET /hub/health (@10.0.0.113) 1.61ms
   [I 2019-10-13 19:27:16.957 JupyterHub log:174] 200 GET /hub/health (@10.0.0.113) 1.49ms
   ...
   ```
   This gives the logs of a pod, useful for debugging when something goes wrong with a pod.

Here's a [reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)
of possible commands.

### IPMI

IPMI is a tool that helps us manage machines remotely. It is essentially a mini-processor sitting alongside the actual server and can help you do a reboot of the system if the main OS becomes unresponsive. It can also be used to reinstall the OS, and control the machine with a mouse/keyboard as if you are in the server room. It's very useful for managing the machines remotely.

If you are using Linux with an X based window manager, Kevin has made a [Docker container](https://hub.docker.com/r/rkevin/ipmihell) that allows you to access the IPMI web interface and remote control the machines.

Some helpful commands that you can run on the management node (rooster or gravity):

`ipmitool -H [IP address] -I lanplus -U ADMIN [command]`: Run an IPMI command on a remote host. You will need a password to do this.

`sudo ipmitool [command]`: Run an IPMI command on this machine.

`ipmitool chassis power reset`: Power cycles the machine.

`ipmitool sol activate`: Activates a serial console to talk to the remote machine.

`ipmitool lan print`: Prints out IPMI networking information.

`ipmitool chassis bootdev [cdrom/bios/disk/...]`: Change the boot device temporarily for the next boot.
