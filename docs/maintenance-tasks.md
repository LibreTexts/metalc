# Maintenance Tasks

This document lists all tasks that should be done regularly.

## Scrub Checks on Blackhole (ZFS)

* Frequency: monthly
* Command: `sudo zpool scrub nest`

To execute manually, you must first ssh into blackhole 
Scrub checks the file system's integrity, and repairs 
any issues that it finds. After the scrub is finished, 
it is good to also run `zpool status` to check if there 
is anything wrong.

This command was previously run on a cronjob. The cronjob ran at 8:00AM 
the first day of every month. Gravity would also send out an 
email at 8:10AM on the same day with the results. If the 
scrub is fine, the email would be titled 
`[All clear] Hen monthly ZFS report`. If the title 
says `[POTENTIAL ZFS ISSUE]` instead, there may be 
something wrong with the disk, and the email contains 
the `zpool status` output which can be used to debug disk 
issues. Details on how the cronjob was setup are in the 
private configuration repo, under `cronjob/monthly-zfs-report.py`.

## Cluster control plane upgrade

The Kubernetes control plane should be upgraded regularly. 
There used to be a cronjob sending out a triyearly reminder 
(Jan, May, Sept 1st of every year) reminding you to do the 
upgrade. (The cronjob can be found in galaxy-control-repo.) 

This must be done at least once a year, otherwise the 
Kubernetes certificates may expire, which will 
[break the entire cluster](/docs/Bare-Metal/troubleshooting/KubeadmCert.md#more-complex-solution-renewing-kubeadm-certificates). 
The email sent out contains the date on which the 
certificates expire. If you apply routine upgrades, 
certificates should be renewed automatically and this 
should not be an issue. If the certificates do expire, 
follow that guide instead of this one. If you need to 
renew the certificates without upgrading the cluster, 
follow [the guide to renew certificates without upgrading](#renew-certificates-without-upgrade) 
instead, but this should not be an excuse to put off 
cluster upgrades indefinitely.

### Upgrading the control plane

tl;dr: Follow https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/ and upgrade the control planes, update apt packages on the nodes, then copy `/etc/kubernetes/admin.conf` on a nebula into `/home/milky/.kube/config` on gravity.

Note: This will take a while and will cause some downtime. Be sure to notify users beforehand.

1. Follow the instructions in the [official cluster upgrade guide](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/). We have multiple control plane nodes (nebulas), so follow both the "Upgrade the first control plane node" and "Upgrade additional control plane nodes" sections. Also follow "Upgrade worker nodes" on all other worker nodes. This is also a good time to [upgrade all packages on the stars](https://github.com/LibreTexts/metalc/blob/447a459bacfbc6a29d80229e7df2f2bfb953cd7a/docs/updating-ubuntu-kubelet.md) as well, since the stars are cordoned during the upgrade.
2. Once you verified the cluster is working using `kubectl get nodes` on gravity/quantum, copy over the newer admin certificate/key.
   1. SSH into a nebula, then do `sudo cp /etc/kubernetes/admin.conf /home/milky/.kube/config`. Also `chown milky:milky /home/milky/.kube/config` to make it readable to us.
   2. Go back into gravity and do `scp nebula{1,5}:.kube/config ~/.kube/config` to copy the file onto gravity.
   3. Verify `kubectl` works on both gravity and the nebulas by running any kubectl command (such as `kubectl get nodes`).

### Renew certificates without upgrade

Sometimes you want to renew the certificates without doing a proper upgrade and causing downtime. In that case, do the following:

1. Follow [the official guide](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/#manual-certificate-renewal). tl;dr: Just run `sudo kubeadm alpha certs renew` on all of the nebulas.
2. Follow the same step 2 as [Upgrading the control plane](#upgrading-the-control-plane).
