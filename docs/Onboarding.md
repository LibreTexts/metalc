# Onboarding

This file helps onboard new hires into the Jupyter team. We currently maintain
[jupyter.libretexts.org](https://jupyter.libretexts.org), a JupyterHub for
LibreTexts and UC Davis users.

# HR

Your immediate supervisors are:

- Jason K. Moore
- Richard Feltstykket

You can reach out to them about any issues you need to discuss. If you don't
feel comfortable reaching out to them (like if you need to report something
about them) you can reach out to their supervisors. Jason's is Cristina Davis
(MAE Chair) and Richard's is Matt Settles.

If you are hired under the MAE department (paid via LibreTexts grant) then you
can contact Felicia Smith in MAE to discuss any HR issues. Felicia is Jason's
account and department manager. You may also have to interact with Chemistry
because that is where the funds are located that pay you.

If you are hired under the Bioinformatics Core (paid by their funds) then you
can contact these people about HR:

- Matt Settles (Richard's Supervisor and your hours approver)
- Ernie Hoftyzer eahoftyzer@ucdavis.edu (Setup your hiring)

## Getting Started

### Connecting to Rooster

The cluster is under a private network, so the only way to access the cluster
is by SSHing into rooster, our management server.

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

Ask us in person for the username and password.

### Joining Our Communication Channels

We use Slack and Zulip to communicate. Make sure that you get invited to
both of these channels.

We also have a shared Google Drive (which is pretty inactive).

### Exchange Phone Numbers and Emails

If you haven't already, please request to add yourself to the 
mailing list: jupyterteam@ucdavis.edu. All emails sent to this address
will be sent to you. This email address is a support email for LibreTexts
and UC Davis users if they encounter any problems with JupyterHub and 
a way for all associated employees to communicate with each other.

[This Google document](https://docs.google.com/document/d/1dXeBmY8jEpVsvfAfu4JYSyvXageEi2URO9XS-0bdsHY/edit#)
has everyone's contact information; feel free to add yours.

### AIOs

Everyone working in Jason's lab sends weekly AIO's over email. We typically
send one email as a team. AIO stands for "Accomplishments, Issues, and
Objectives." More info about AIO's can be found
[here](https://mechmotum.github.io/guide.html).

## Logging Your Hours

Once you get hired, you will log your hours on
[trs-ucpath.ucdavis.edu](https://trs-ucpath.ucdavis.edu). You should also
receive a key card which can get you access to the server room. Matt Settles
can give you key card access.

## Working on GitHub

We document our work on GitHub. This is so that any current or future workers
can refer back to the work already done.

There are a couple of repositories we use:
* [metalc](https://github.com/LibreTexts/metalc/) is the main repository. It contains
information on how to build the bare metal cluster using VMs, Google Cloud, and 
most importantly on bare-metal. [Baremetal.md](https://github.com/LibreTexts/metalc/blob/master/docs/Bare-Metal/baremetal.md)
is the cumulative document that combines all information about building 
the cluster.
* [default-env](https://github.com/LibreTexts/default-env) contains Dockerfiles for
creating the Default Environment in JupyterHub.
* [ckeditor-binder-plugin](https://github.com/LibreTexts/ckeditor-binder-plugin) is a plugin which lets
LibreTexts authors add executable code-blocks into the LibreTexts text editor. LibreTexts uses CKEditor
for its text editor; thus our plugin uses the CKEditor API.

Some less frequently updated repositories:
* [mechmotum.github.io](https://github.com/LibreTexts/mechmotum.github.io) is our fork 
of Jason's website. We write blog posts on this fork and later make pull requests to 
merge on his repository.
* [jupyterhub-templates](https://github.com/LibreTexts/jupyterhub-templates) 
contains custom HTML pages for the website. Updating these on GitHub will
update the website if JupyterHub gets upgraded.
* [jupyterhub-images](https://github.com/LibreTexts/jupyterhub-images)
constains images used on the website.

We track our current tasks on [Issues](https://github.com/LibreTexts/metalc/issues).
Feel free to assign yourself to an issue!

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

### Grafana
Our alerting and monitoring system is based in grafana.libretexts.org.

### Quick Guide to Navigating Kubernetes
`kubectl` is the main way for us to get information from Kubernetes via the command line.
After you SSH into rooster, try out a few of the following `kubectl` commands:

1. `kubectl get nodes`
  ```
  NAME      STATUS                     ROLES    AGE    VERSION
  chick0    Ready                      master   121d   v1.16.1
  chick1    Ready                      <none>   121d   v1.14.0
  chick10   Ready                      <none>   114d   v1.14.0
  chick11   Ready                      <none>   9d     v1.14.0
  chick12   Ready                      <none>   8d     v1.14.0
  chick13   Ready                      <none>   8d     v1.14.0
  chick14   Ready                      <none>   8d     v1.14.0
  chick15   Ready                      <none>   8d     v1.14.0
  chick16   Ready                      <none>   8d     v1.14.0
  chick17   Ready                      <none>   8d     v1.14.0
  chick18   Ready                      <none>   8d     v1.14.0
  chick2    Ready                      <none>   121d   v1.14.0
  chick3    Ready                      <none>   121d   v1.14.0
  chick4    Ready,SchedulingDisabled   <none>   121d   v1.14.0
  chick5    Ready,SchedulingDisabled   <none>   121d   v1.14.0
  chick6    Ready,SchedulingDisabled   <none>   121d   v1.14.0
  chick7    Ready                      <none>   121d   v1.14.0
  chick8    Ready                      <none>   121d   v1.14.0
  chick9    Ready                      <none>   121d   v1.14.0
  ...
  ```
  This shows all of the nodes on the cluster. You can see the status of each.
  Note that chick0 is labeled as `master`.
  Also note that some chicks are labeled `SchedulingDisabled`; this means that
  no pods can get scheduled onto these nodes.

1. `kubectl get pods -A`
   ```
   NAMESPACE        NAME                                                        READY   STATUS        RESTARTS   AGE
   binderhub        autohttps-59dd446c76-59mbn                                  2/2     Running       0          52d
   binderhub        binder-5696db87dc-2qll2                                     1/1     Running       0          26d
   binderhub        binderhub-image-cleaner-2qlsm                               1/1     Running       0          8d
   ...
   ```
   This outputs all of the pods currently on the cluster.
  
1. `kubectl get pods -n jhub`
   ```
   NAME                                 READY   STATUS    RESTARTS   AGE
   autohttps-7b4fb9dd6b-gb6td           2/2     Running   0          25d
   continuous-image-puller-7h4jr        1/1     Running   0          32h
   continuous-image-puller-7mv45        1/1     Running   0          32h
   ...
   ```
   This outputs all the pods in the `jhub` namespace. The `jhub` namespace contains
   pods related to our JupyterHub instance.
  
1. Now try logging into JupyterHub and spawn a server. Run `kubectl get pods -n jhub` again.
   You should see a new pod with the name `jupyter-<your email>`.
   ```
   NAME                                            READY   STATUS    RESTARTS   AGE
   ...
   jupyter-<username of email>-40ucdavis-2eedu     1/1     Running   0          1m
   ...
   ```
  
1. `kubectl describe pod hub-<fill in random string you get from kubectl get pods here> -n jhub`
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
   
1. `kubectl exec hub-<fill in random string you get from kubectl get pods here> -n jhub -ti bash`
   ```
   jovyan@hub-<random string>:/srv/jupyterhub$
   ```
   This lets you enter the pod and use its command line. You can explore the directories here
   to see what kind of files are used. This pod is almost like running the original 
   [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/) without knowledge of Kubernetes.
   Type `exit` to exit the pod.
  
1. `kubectl logs hub-<fill in random string you get from kubectl get pods here> -n jhub`
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
