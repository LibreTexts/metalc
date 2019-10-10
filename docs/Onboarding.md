# Onboarding

This file helps onboard new hires into the Jupyter team.

## Getting Started
### Connecting to Rooster
The cluster is under a private network, so the only way to access the cluster is by 
SSHing into rooster, our management server.

If you have Windows, it would probably be easier to 
install [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
PuTTY makes it easier for you to SSH into rooster. Otherwise, you can
use the command line.

You need to give your public key to someone who currently has access
to rooster so that you can SSH into the server. 
[Generate your SSH key](https://confluence.atlassian.com/bitbucketserver/creating-ssh-keys-776639788.html)
if you haven't already. If you are using PuTTY, generate your SSH key
using [PuTTYGen](https://www.ssh.com/ssh/putty/windows/puttygen). 

Afterwards, email your public key (should be the file `id_rsa.pub`
or something similar) to someone who has access to rooster. **Do not
email your private key.**

### Joining Our Communication Channels
We use Slack and Zulip to communicate. Make sure that you get invited to
both of these channels.


### Exchange Phone Numbers and Emails
If you haven't already, please request to add yourself to the 
mailing list: jupyterteam@ucdavis.edu. All emails sent to this address
will be sent to you. This email address is a support email for LibreTexts
and UC Davis users if they encounter any problems with JupyterHub and 
a way for all associated employees to communicate with each other.

[This Google document](https://docs.google.com/document/d/1dXeBmY8jEpVsvfAfu4JYSyvXageEi2URO9XS-0bdsHY/edit#)
has everyone's contact information; feel free to add yours.

## Working With the Cluster
Our bare-metal cluster consists of one master node named chick0 and 20 children named 
chick1 through chick19 sequentially. It also contains a management node called rooster, which 
acts as a proxy between the Internet and the cluster. 

### Kubernetes
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

### JupyterHub
**JupyterHub** is a service that allows multiple users to create notebooks with code.

[Zero to JupyterHub with Kubernetes](https://zero-to-jupyterhub.readthedocs.io/en/latest/)
is the main documentation for building a JupyterHub cluster from Kubernetes.
You can try to build your own on Google Cloud, but this will cost money
(*unless*: if you have not used Google Cloud before, you can get $300 free credits).

If you want to know more about what Jupyter is, visit [https://try.jupyter.org](try.jupyter.org).


