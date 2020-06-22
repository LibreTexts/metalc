# Troubleshooting JupyterHub

A guide on what to do when you can't access the front page, a user can't
spawn a server, and other mishaps.

### Generally...
Your process for troubleshooting issues is:
1. `kubectl get <resource>`
1. `kubectl describe <resource>`
1. If you cannot identify and fix the problem without deleting the resource,
then delete it. `kubectl delete <resource>`
   1. If you think a node caused this issue, then drain it. `kubectl
   drain <node>`. Sometimes, this command doesn't complete because important
   system pods are running on the node; this is okay.
1. Upgrade JupyterHub. Navigate to `~/jupyterhub` and run `upgrade.sh`.
   1. Sometimes, JupyterHub doesn't like the upgrade script, and we don't
   know why. In this case, just copy and paste the commands to the terminal:
   ```
   RELEASE=jhub

   helm upgrade $RELEASE jupyterhub/jupyterhub \
     --version=0.9-2d435d6 \
     --values config.yaml
   ```

## Table of Contents
1. [JupyterHub is down](#JupyterHub-is-down)
1. [A user cannot spawn a server](#A-user-cannot-spawn-a-server)
1. [A node is acting strangely](#A-node-is-acting-strangely)
1. [JupyterHub fails to upgrade](#JupyterHub-fails-to-upgrade)
1. [Removing a node from the cluster](#Removing-a-node-from-the-cluster)
1. [JupyterHub fails to upgrade](#JupyterHub-fails-to-upgrade)
1. [`kubectl` doesn't work`](#kubectl-doesn't-work)
1. [Website is giving an SSL error](#website-is-giving-an-ssl-error)
1. [Resources](#Resources)

## JupyterHub is down
First, scream.

Second, execute `kubectl get nodes -n jhub` in rooster. You should see
something like this:
```
hub-xxxxxxxx-xxxxx                 1/1     Running                 0          142m
proxy-xxxxxxxx-xxxxx               1/1     Running                 0          41d
autohttps-xxxxxxxx-xxxxx           2/2     Running                 0          16d
```

Check the `hub-xxx` pod especially. Is it Running?

If not, describe the pod using `kubectl describe hub-xxx -n jhub`. Check the logs
under `Events`. Often, you can find the cause of the problem and solve it appropriately.

* "There's not enough ephermeral storage." Usually this means that there's isn't
enough hard drive/SSD storage on the disk.
* "Readiness probe failed." Sometimes, if you upgrade, this will fix the problem. In the past,
waiting for 2 minutes resolved the problem on its own. If this doesn't work, the hub pod might
be on a bad node.

If all else fails, upgrade JupyterHub. Be aware that upgrading JupyterHub does
not necessarily recreate JupyterHub-related pods if you didn't change `config.yaml`.
If necessary, upgrade with the flag `--recreate-pods`, which forces the recreation
of JupyterHub-related pods.

An alternative method is to delete the `hub-xxx` pod manually by calling `kubectl
delete pod hub-xxx -n jhub`, which will delete the existing hub pod and automatically
create a new one.

## A user cannot spawn a server
References:
* [This issue](https://github.com/LibreTexts/metalc/issues/35) details what happens
when a node goes down and a user pod was running on it.

Run `kubectl get pods -n jhub`. What state is the user's pod in?

If the pod is not in a `Terminating` state, try deleting the pod by running
`kubectl delete pod <userpod name>`.

If it's in a `Terminating` state but the pod did not delete itself, or if you cannot delete
the pod for whatever reason, this usually means there is a problem with the node.
SSH into the node and check whether the [drives are okay](#A-node-is-acting-strangely).
Another possibility is thatthe Docker containers failed to terminate, which causes
the pods to not terminate. Try restarting the node or upgrading JupyterHub.

Try running `kubectl delete pod hub-xxx -n jhub` to restart the `hub-xxx` pod. If
you know there is nothing wrong with the cluster itself, then this should be relatively
safe and the hub pod will restart on its own.

If that doesn't work, try upgrading JupyterHub by running `upgrade.sh` or copying and
pasting the following commands. This is slightly more riskier since you are applying
`config.yaml` to the hub. This means that any changes to `config.yaml` will be applied.
   ```
   RELEASE=jhub

   helm upgrade $RELEASE jupyterhub/jupyterhub \
     --version=0.9-2d435d6 \
     --values config.yaml
   ```


## A node is acting strangely
Check whether the drives are okay:
* `lsblk` to see if the partitions still exist.
* `smartctl -a /dev/sda` or `smartctl -a /dev/sdb` to check the status of the drives.
If the `Reallocated_Sector_Ct` is 0 then it's good.
* `smartctl -t short /dev/sda` or `smartctl -l selftest /dev/sda` to run a test on the
drives.

## Removing a node from the cluster
**Important: This should be the last resort**  
If non of the other troubleshooting methods resolved the issue on a node, and the issue is
affecting the performance of the cluster then it is best to remove such node from the cluster
to restore the services.
1. Unschedule the node so that no new pods can be scheduled on the problematic node with `kubectl drain chick<i>`, where i is the node number.
1. Check if the node is running some critical pods with the command `kubectl get pods -A -o wide | grep "chick<i>"`,
where i is a chick number, this will display all the pods that are running on that specific chick.
A critical pod is a pod that is involved in serving any of our public facing services or our monitoring services or anything
else that you think is important. Some examples are: autohttps, binder, hub, proxy, nfs-client-release-nfs-client-provisioner,
quickstart-nginx.
1. Remove the critical pods on the node so that they get rescheduled somewhere else `kubectl delete pods <name of the pod> -n <namespace>`
1. Make sure the pods have been rescheduled to another node by running `kubectl get pods -n <namespace> -o wide` and you should see the pod
starting on another node.
1. Run `kubectl delete node chick<i>`, where i is the number of the node, to remove the node from the Kubernetes cluster.

## JupyterHub fails to upgrade
Unfortunately, running `helm upgrade` does not give a lot of debugging information
when an upgrade fails.
There are a couple possible causes for a failed upgrade, including but not limited to:

1. `config.yaml` isn't written correctly. These are the most common problems:
   1. Spelling errors. For example, if you mispell a Docker image name or a name,
   JupyterHub will fail to upgrade.
   1. Tab/spacing errors. Double check that your spacing is correct. We indent our YAML
   files with two spaces.

   JupyterHub is picky when reading `config.yaml`. For example,
   1. It doesn't like when you leave in lines of comments between lists of items like emails.

      This is bad:
      ```
         - chihuahua@ucdavis.edu
         # Under the deep blue sea
         - octopus@gmail.com
         - platypus@gmail.com
      ```

      This is OK:
      ```
         - chihuahua@ucdavis.edu
         - octopus@gmail.com # Under the deep blue sea
         - platypus@gmail.com
      ```

   1. In the `extraConfig` section, you can attach extra Python code to specific keys.
      `config.yaml` sometimes doesn't like when you add comments in this section

      Example:
      ```
      extraConfig:
         templates: |
            c.JupyterHub.template_paths = ['/etc/jupyterhub/custom/custom']
            # Wow a comment like this might cause problems

1. The cluster is preventing an upgrade (less common).
   1. [This issue](https://github.com/LibreTexts/metalc/issues/75) details how
   an unschedulable chick contained `hook-image-puller` and `continuous-image-puller` pods
   that were always in a `Pending` state. Since JupyterHub requires these pods
   to finish running to complete an upgrade, pending pods would stall the
   upgrade.

## `kubectl` doesn't work
*Main article: [KubeadmCert.md](KubeadmCert.md)*
```
$ kubectl get nodes
The connection to the server <host>:6443 was refused - did you specify the right host or port?
```

* After a server is restarted, sometimes swap is turned back on if it is not specified in
`/etc/fstab`. Swap does not work with Kubernetes, so simply SSH into that server, run
`sudo swapoff -a`, and wait a couple of seconds.

* More rarely, kubeadm certificates expire after one year exactly if their
  renewals are not activated, causing the master node to stop responding.
  More information on how to renew these certificates in
  [KubeadmCert.md](KubeadmCert.md).

For more information, see [this Kubernetes Forum issue](https://discuss.kubernetes.io/t/the-connection-to-the-server-host-6443-was-refused-did-you-specify-the-right-host-or-port/552/5)
and possibly [this issue](https://github.com/LibreTexts/metalc/issues/87).


## Website is giving an SSL error
*Main article: [HTTPSonJupyterHub.md](HTTPSonJupyterHub.md)*
JupyterHub and BinderHub require port 80 to be open in order for certificates
to be accepted. By default, in NGINX we redirect HTTP requests to
HTTPS requests. However, if you are installing JupyterHub or BinderHub
from the beginning, Let's Encrypt will not be able to assign a certificate
without accepting HTTP requests.

## Resources
We use the following resources for troubleshooting JupyterHub problems:
* [Jupyter Discourse Forum](https://discourse.jupyter.org/) 
  has a lot of questions answered by Jupyter developers
* Jupyter documentation can also explain what might 
  be happening if you're stuck
  * [Zero to JupyterHub](https://zero-to-jupyterhub.readthedocs.io/en/latest)
  * [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/)
  * JupyterHub uses other pieces such as [Kubespawner](https://jupyterhub-kubespawner.readthedocs.io/en/latest/spawner.html).
* [Zero to JupyterHub GitHub issues](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues)
* Googling 
