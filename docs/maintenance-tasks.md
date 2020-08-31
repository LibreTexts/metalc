# Maintenance Tasks

This document lists all tasks that should be done regularly.

## Security Update on Rooster

* Frequency: weekly
* Command: `sudo unattended-upgrade -d`

Rooster is the only server that has a public network. It is essential to keep the system up to date. We use [unattended-upgrade](https://github.com/mvo5/unattended-upgrades) to upgrade packages safely. To minimize affecting the cluster, check the following before running the command:

1. Run `sudo unattended-upgrade -d --dry-run` to make sure that it will upgrade without error.
2. Check `kubectl get pods -n jhub` to see if there are a lot of people using the cluster. Try to upgrade when no one is there.

Additionally, there is a cron job on rooster that runs `sudo unattended-upgrade -d --dry-run` and sends out weekly emails on Friday. Do `sudo crontab -e` to edit the cron job. If you wish to change the code of the cron job, the shell script is located at `/home/spicy/metalc-configurations/cronjob/weekly-security-update`. The shell script is a python script that uses pipes to run commands.

## Scrub Checks on Hen (ZFS)

* Frequency: monthly
* Command: `sudo zpool scrub nest`

To execute manually, you must first ssh into hen from rooster with the command `ssh hen`. Scrub checks the file system's integrity, and repairs any issues that it finds. After the scrub is finished, it is good to also run `zpool status` to check if there is anything wrong.

This command is run on a cronjob, so there should be no need for manual intervention. The cronjob runs at 8:00AM the first day of every month. Rooster will also send out an email at 8:10AM on the same day with the results. If the scrub is fine, the email should be titled `[All clear] Hen monthly ZFS report`. If the title says `[POTENTIAL ZFS ISSUE]` instead, there may be something wrong with the disk, and the email contains the `zpool status` output which you can use to debug disk issues. Details on how the cronjob is setup are in the private configuration repo, under `cronjob/monthly-zfs-report.py`.

## Cluster control plane upgrade

The Kubernetes control plane should be upgraded regularly. There is a cronjob sending out a triyearly reminder (Jan, May, Sept 1st of every year) reminding you to do the upgrade. (The cronjob can be found in the private configuration repo, under `cronjob/cluster-upgrade-reminder.sh).

This must be done at least once a year, otherwise the Kubernetes certificates may expire, which will [break the entire cluster](https://github.com/LibreTexts/metalc/blob/master/docs/Bare-Metal/troubleshooting/KubeadmCert.md#more-complex-solution-renewing-kubeadm-certificates). The email sent out should contain the date on which the certificates expire. If you apply routine upgrades, certificates should be renewed automatically and this should not be an issue. If the certificates do expire, follow that guide instead of this one. If you need to renew the certificates without upgrading the cluster, follow [the guide to renew certificates without upgrading](#renew-certificates-without-upgrade) instead, but this should not be an excuse to put off cluster upgrades indefinitely.

### Upgrading the control plane

tl;dr: Follow https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/ and upgrade the control plane, update apt packages on the nodes, then copy `/etc/kubernetes/admin.conf` on chick0 into `/home/spicy/.kube/config` on rooster.

Note: This will take a while and will cause some downtime. Be sure to notify users beforehand.

1. Follow the instructions in the [official cluster upgrade guide](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/). We only have one control plane node (chick0), so follow the "Upgrade the first control plane node" secion on chick0 and ignore "Upgrade additional control plane nodes". Also follow "Upgrade worker nodes" on all other chicks. This is also a good time to [upgrade all packages on the chicks](https://github.com/LibreTexts/metalc/blob/447a459bacfbc6a29d80229e7df2f2bfb953cd7a/docs/updating-ubuntu-kubelet.md) as well, since the chicks are cordoned during the upgrade.
2. Once you verified the cluster is working using `kubectl get nodes` on rooster, copy over the newer admin certificate/key.
   1. SSH into chick0, then do `sudo cp /etc/kubernetes/admin.conf /home/spicy/.kube/config`. Also `chown spicy:spicy /home/spicy/.kube/config` to make it readable to us.
   2. Go back into rooster and do `scp chick0:.kube/config ~/.kube/config` to copy the file onto rooster.
   3. Verify `kubectl `works on both rooster and chick0 by running any kubectl command (such as `kubectl get nodes`).

### Renew certificates without upgrade

Sometimes you want to renew the certificates without doing a proper upgrade and causing downtime. In that case, do the following:

1. Follow [the official guide](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/#manual-certificate-renewal). tl;dr: Just run `sudo kubeadm alpha certs renew` on chick0.
2. Follow the same step 2 as [Upgrading the control plane](#upgrading-the-control-plane).
