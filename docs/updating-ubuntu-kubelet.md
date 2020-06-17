# Updating Ubuntu

This document lists the procedure for updating Ubuntu on the chick nodes, except for chick0.

## Checking Software Versions on the Nodes

You can check the versions of kubelet, Ubuntu and the kernel as well as the status of each node by executing the command `kubectl get nodes -o wide` from rooster. Due to reasons stated [here](https://github.com/kubernetes/kubernetes/issues/86094), you should make sure that each kubelet version is no greater than v1.16.10, and you should not upgrade past this version.

## Preparing to Update

1. Before you even begin to update a given node, check which pods are running on it with the command `kubectl get pods -A -o wide | grep 'chick#'`, where # is replaced with the number of the chick ie. chick1, chick2, chick3, etc. If there are non-default pods running on that node, you should wait for them to shutdown. *If* you have permission to do so, you may manually delete them with `kubectl delete pod <insert pod name here> -n <insert namespace here>`.
2. If the node does not have any critical processes running on it, you may mark the node as unschedulable with the command `kubectl cordon chick#`. This ensures that no new pods are spawned while you are updating the node. 
	- To make sure this was done correctly, run `kubectl get nodes` and check that the `STATUS` column says `SchedulingDisabled` for that node.
3. Next you will remove all pods from it with `kubectl drain chick#`. You may have to use flags `--ignore-daemonsets` and `--delete-local-data` with the in order to drain the default  pods. 
	- If you are prompted to use the `--force` command, then you have a non-default pod which you must wait to shutdown or receive permission to delete. You should return to step 1 in this case.

## Updating the Node

Once the node has been cordoned and drained, you may ssh into it with `ssh chick#`. From there, you will install the updates.

1. Run `sudo apt update` before any other commands. This ensures that the repositories for the node contain all the most recent files for you to install.
2. If necessary, upgrade kubelet to v1.16.10 with `sudo apt upgrade kubelet=1.16.10-00`. We do this independently of all the rest because of version compatibility issues past v1.17. The terminal will prompt you about auto-restarting processes during the upgrade. You may choose 'yes'. This upgrade may take a few minutes.
3. After this upgrade is complete, ensure that kubelet does not update again with `sudo apt-mark hold kubelet`. 
4. Finally, run `sudo apt upgrade`. This will upgrade all the packages from `sudo apt --upgradable` *except* for kubelet, which we pinned to v1.16.10 in step 3. This upgrade should be very quick.
5. After the upgrade is complete, the node will require a reboot with `sudo reboot`. 
6. Once the reboot is complete, you should uncordon the node from rooster with `kubectl uncordon chick#`. 
	- Make sure that this occurred properly with `kubectl get nodes -o wide` and checking under the `STATUS` column, where the node should say `Ready` after it has rebooted, and there should be no `SchedulingDisabled` message. 
7. Ensure that everything upgraded properly by checking with `kubectl get nodes -o wide`. Make sure the `OS-IMAGE` and `VERSION` columns display the correct version you were upgrading to. 

## More Information and Troubleshooting

The official documentation for upgrading kubelet is available [here](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/). If the node does not show that it is `Ready` after the reboot, then you should ssh back into the node and check the status of kubelet and docker with `systemctl status kubelet` or `systemctl status docker` to see if there are any errors. You may first want to try restarting with `sudo systemctl restart kubelet` for instance, if the node's status is `NotReady`.