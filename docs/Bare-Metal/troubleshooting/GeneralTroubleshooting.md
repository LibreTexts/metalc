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
