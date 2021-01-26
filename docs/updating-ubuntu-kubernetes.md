# Updating Ubuntu and Kubernetes

This document lists the procedure for updating Ubuntu and 
Kubernetes on the chick nodes.

## Checking Software Versions on the Nodes

You can check the versions of kubernetes, Ubuntu and the 
kernel as well as the status of each node by executing the 
command `kubectl get nodes -o wide` from rooster. When you 
do Kubernetes upgrades, make sure that you do not upgrade 
more than one minor version at a time. For example, if the 
cluster is at verison 1.19 and the latest available version 
is 1.21, you should first upgrade everything to 1.20, then 1.21.

## Preparing to Update

1. Before you even begin to update a given node, check which pods are running on it with the command `kubectl get pods -A -o wide | grep 'chick#'`, where # is replaced with the number of the chick ie. chick1, chick2, chick3, etc. If there are non-default pods running on that node, you should wait for them to shutdown. *If* you have permission to do so, you may manually delete them with `kubectl delete pod <insert pod name here> -n <insert namespace here>`.
2. If the node does not have any critical processes running on it, you should mark the node as unschedulable with the command `kubectl cordon chick#`. This ensures that no new pods are spawned while you are updating the node. 
	- To make sure this was done correctly, run `kubectl get nodes` and check that the `STATUS` column says `SchedulingDisabled` for that node.
3. Next you will remove all pods from it with `kubectl drain chick#`. You may have to use flags `--ignore-daemonsets` and `--delete-local-data` with the drain command in order to drain the default  pods. 
	- If you are prompted to use the `--force` command, then you have a non-default pod which you must wait to shutdown or receive permission to delete. You should return to step 1 in this case.

## Updating Kubernetes

The official documentation for upgrading Kubernetes is available 
[here](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/). 
You will first have to upgrade kubeadm and then use it to 
upgrade kubelet and kubectl. The processis pretty straightforward 
if you follow the official documentation. Also checkout 
`maintenance-tasks.md` for more information about cluster 
upgrades and nuances. 

## Updating Ubuntu

Once the node has been cordoned and drained, you may ssh into it with `ssh chick#`. From there, you will install the updates.

1. Run `sudo apt update` before any other commands. This ensures that the repositories for the node contain all the most recent files for you to install.
4. Run `sudo apt upgrade`. This will upgrade all the packages from `sudo apt --upgradable`.
5. After the upgrade is complete, the node may require a reboot with `sudo reboot`. 
6. Once the reboot is complete, ensure that everything upgraded properly by checking with `kubectl get nodes -o wide`. Make sure the `OS-IMAGE` and `VERSION` columns display the correct versions of Ubuntu and kubelet you were upgrading to. 
7. Finally, if all upgrades have occurred properly, you should uncordon the node with `kubectl uncordon chick#`. 
	- Make sure that this occurred properly with `kubectl get nodes -o wide` and checking under the `STATUS` column, where the node should say `Ready` and there should be no `SchedulingDisabled` message. 

## More Information and Troubleshooting

If the node does not show that it is `Ready` after the reboot, then you should ssh back into the node and check the status of kubelet and docker with `systemctl status kubelet` or `systemctl status docker` to see if there are any errors. You may first want to try restarting with `sudo systemctl restart kubelet` for instance, if the node's status is `NotReady`.
