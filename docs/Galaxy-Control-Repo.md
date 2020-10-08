# Galaxy Control Repo

This document is largely copy+pasted directly from the README.md of our private puppet control-repo for the Galaxy Cluster. We have repurposed it for public viewing here.

## Initial setup

All nodes are using Ubuntu 20.04.

### Setting up the puppet server (gravity)

```sh
# install puppetserver
wget https://apt.puppetlabs.com/puppet6-release-bionic.deb
sudo dpkg -i puppet6-release-bionic.deb
sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y
sudo apt install -y puppetserver

# start puppet server and puppet agent service
sudo systemctl enable puppetserver && sudo systemctl start puppetserver
sudo /opt/puppetlabs/bin/puppet resource service puppet ensure=running enable=true

# install r10k, which deploys the control repo
sudo /opt/puppetlabs/puppet/bin/gem install r10k
```

Afterwards, set up the r10k config at `/etc/puppetlabs/r10k/r10k.yaml`:
```
# The location to use for storing cached Git repos
:cachedir: '/var/cache/r10k'

# A list of git repositories to create
:sources:
  # This will clone the git repository and instantiate an environment per
  # branch in /etc/puppetlabs/code/environments
  :galaxy-development:
    remote: 'galaxy-control-repo:LibreTexts/galaxy-control-repo'
    basedir: '/etc/puppetlabs/code/environments'
```

You will also need to configure rooster's SSH keys so it can pull protogalaxy and galaxy-control-repo. To work around GitHub requiring all deploy keys to be different, we actually have two SSH keys as root, and a `/root/.ssh/config` file like this:
```
Host galaxy-control-repo
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_galaxy_control_repo
Host protogalaxy
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa
```
Your configuration may differ.

If you are not using the "production" branch of the repo, you should also change the default environment. Edit `/etc/puppetlabs/puppet/puppet.conf` and add the following if you want to use the "development" branch:

```
[master]
environment = development

[agent]
environment = development
```

Finally, you may do your first puppet run using `sudo r10k deploy environment -p && sudo puppet agent -t`.

### Setting up each puppet agent

First, we need to add an entry in `/etc/hosts`:
```
10.0.0.113	gravity	puppet
```
This allows this server to know where the puppet server is (in this case 10.0.0.113). Afterwards:

```
# install puppet agent
wget https://apt.puppetlabs.com/puppet6-release-bionic.deb
sudo dpkg -i puppet6-release-bionic.deb
sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y
sudo apt install puppet-agent

# start puppet agent service
sudo /opt/puppetlabs/bin/puppet resource service puppet ensure=running enable=true
```

Also, edit `/etc/puppetlabs/puppet/puppet.conf` and add the following if you're using a branch not called `production`, for example `development`:

```
[agent]
environment = development
```

This won't immediately work yet, since gravity must sign the certificates.

### Signing agent certificates

Run the following on gravity: `sudo puppetserver ca list`. You should see a list of certificate requests, one from each puppet agent you setup. You can then do a `sudo puppetserver ca sign --all` to sign all the certifiates. Now the puppet agents can pull down the configuration files.

## Making changes to the puppet code

Follow the directory structure when adding new code. You can use `puppet parser validate <file.pp>` to validate any puppet code you write. This won't guarantee the code works, but at least you know there won't be any syntax errors.

A good way to make sure your code never has syntax errors is to add the following as a pre-commit hook:

```sh
#!/bin/bash
find|grep '\.pp$'|xargs puppet parser validate
```

Save this script as `.git/hooks/pre-commit`, `chmod +x .git/hooks/pre-commit`, and every time you try to commit it will warn you about errors and stop you from committing bad code. You can always do a `git commit --no-verify` to force a commit.

## Applying configuration changes

You need to first pull the code on gravity:

```sh
sudo r10k deploy environment -p
```

Afterwards, you may manually do a puppet run using the following command on all relevant nodes:

```sh
sudo puppet agent -t --verbose --debug
```

You may omit the `--verbose --debug` flags, but they're useful when your code breaks and you need to figure out why.

Alternatively, all the puppet agents will pull and apply the config from the puppet server every 30 minutes, so just waiting is also a valid alternative if you're sure your code won't break.

## Upgrading the Kubernetes cluster

Since we're using protogalaxy, there are a couple of steps different from the [official upgrade instructions](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/), although the idea is mostly the same. Also note that you may only upgrade one minor version at a time (so for example from 1.17.5 to 1.18.2, but not from 1.16.0 to 1.18.0), so if the cluster is really out of date you might need to repeat this process several times.

### Setting up protogalaxy

In `data/common.yaml`, modify the hiera values `protogalaxy::upgrading_cluster` to be `true`, and `protogalaxy::k8s_version` to be the new desired version. Redeploy everything using `sudo r10k deploy environment -p && sudo puppet agent -t` on gravity and `sudo puppet agent -t` everywhere else.

### Upgrading the first control plane node (nebula1)

Note: all `kubectl` commands should be run on gravity, while all other commands should be run on the node being upgraded.

First, drain the node using `kubectl drain nebula1 --ignore-daemonsets` (you may need to follow additional instructions to delete stubborn pods), then plan the upgrade using `sudo kubeadm upgrade plan`. Make sure the output makes sense (without errors), then you can apply the upgrade using `sudo kubeadm upgrade apply v1.19.2`, replacing the version number with your desired version. Finally, upgrade kubelet using `sudo apt install --allow-change-held-packages kubelet=1.19.2-00`, replacing the version number with your desired version. After a reboot (this is also a pretty good time to do a `sudo apt update && sudo apt upgrade` in general before you reboot), you may uncordon this node using `kubectl uncordon nebula1`.

### Upgrading additional control plane nodes (nebula*) and worker nodes (star*)

This process is exactly the same as upgrading the first control plane node, but do not run `sudo kubeadm upgrade plan` or `sudo kubeadm upgrade apply`. Instead, use `sudo kubeadm upgrade node`. Remember to only do a couple at a time (for control plane nodes, one at a time) so the cluster never goes down.

For those of you who are lazy (like me), here's a oneliner you can copy (excluding the cordon/uncordon part) if you understand every step of the process (remember to change the version number):

```sh
sudo kubeadm upgrade node && sudo apt update && sudo apt install --allow-change-held-packages kubelet=1.19.2-00 && sudo apt upgrade && sudo reboot
```

### Copying the new admin.conf over

(TODO: automate this using puppet somehow?) On nebula1, the `/etc/kubernetes/admin.conf` contains certificates and keys to allow kubectl to talk to the server. After a cluster upgrade, the certificate is renewed, so you have to manually copy it over to gravity. Copy it somewhere temporarily (such as /tmp) and change the ownership so the `ctrl` user can read it (`sudo chown ctrl:ctrl admin.conf`). Afterwards, `scp` it onto gravity like `scp nebula1:/tmp/admin.conf .kube/config`. Finally, delete it from /tmp using `rm /tmp/admin.conf`.

### Trun off upgrade mode on protogalaxy

Change the hiera value `protogalaxy::upgrading_cluster` to `false`. Redeploy it and do a puppet run for good measure, although the puppet run is not really needed.

