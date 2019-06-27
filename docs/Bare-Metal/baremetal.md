# Bare Metal Stuff

This is everything that we need to know to work on the baremetal kubernetes
cluster.

# Summary

1. [Introduction](#Introduction)
1. [Roadmap](#Roadmap)
1. [Networking](#Networking)
1. [Publishing Services](#Publishing-Services)
1. [Netbooting](#Netbooting)
1. [Adding Nodes](#Adding-Nodes)
1. [Literature List](#Literature-List) for learning resources.
1. [Useful Commands](#Useful-Commands)

# Introduction

## Management Node

In the rest of the docs we may refer to the management node by its hostname,
rooster.

This node is not part of the kubernetes cluster, but acts as a gateway to the
internet, runs a dhcp server, and hosts the network boot stuff.

## Standard Nodes

We are calling the basic nodes chicks. These will be our masters and workers in
the kubernetes cluster.

Each has hostname `chick{i}` where i is a natural number.

Currently have `chick0` through `chick10` so 11 in total.

Assinging static IPs for `chick{i}` of `10.0.0.{i + 100}`. So `chick0` will be
at `10.0.0.100` and `chick1` at `10.0.0.101`, etc.

## Testing

try running a [test deployment](
https://github.com/kubernetes/examples/blob/master/staging/simple-nginx.md)
and see if you can access the server from every node. Or if you can accesss the
public ip assigned by metalc from outside the network if you publish as type
loadbalancer.

# Roadmap

Basically, a todo list for the cluster and our development plan for the future.

# Minimum Requirements

## On-Premis Requirements

This is stuff that needs to be done before all work can be done remotely.

- rack all servers and nfs server (remember to put RAM in all servers)
- put disks in the servers
- install OS (can only be done after disks are in)
- wiring for the networking
- networking -- though this technically can be done remotely, we might break
  something while doing it so we should do it on-premis.
  - write down the MAC addresses for the interfaces we use on all the nodes.
    We might also want to assign each node a static IP in our private network
    by changing the dhcp configuration on our management node.
  - pod network fabric
  - metallb (metal load balancer. See below)

## Kubernetes Install

Using kubeadm with the Ansible playbook to install everything. Right now this works in the dev-env,
but we need to get it to bare metal. Preferably set it up so we can use the same playbook for both
the development environment and the actual metal one.

## Network Fabric

We need to set up the network fabric in some way. Flannel is working in dev-env, but it has
a lot of overhead because it uses ip tunneling. Something to consider is Calico, but we may
need some more complicated config

## Persistent Volume Provisioner

This is where we will talk to the nfs server to allow for persistent volumes. It shouldn't be
that different from the nfs-client setup we have in dev-env.

We can either create a default Storage Class, but it would be more secure and give us finer
grained control if we configured all of them manually by passing values to the jupyterhub Helm
chart. In this way we can allow for different persistence and rules within the same cluster, but
it may not be a problem if we just namespace everything into separate namespaces.

## Load Balancer

[MetalLB](https://metallb.universe.tf) seems to be the move for this one. It makes it so when services
are published as type LoadBalancer, they still work on bare metal and IPs are provided automatically.
This seems like the best way to expose services to outside the cluster on bare metal without having
to make any modifications to the underlying helm charts.
Certainly the people at nginx ingress make this seem like the best option in [these docs](
https://kubernetes.github.io/ingress-nginx/deploy/baremetal/)

# Long(er) Term Goals
## HA masters

Down the road, we need to configure high availability masters so we aren't as vulnerable to a master
failing. The setup is outlined in the [kubeadm docs](https://kubernetes.io/docs/setup/independent/high-availability/). 
We can use either [HA proxy](http://www.haproxy.org/#desc), which Richard is familiar with, 
or maybe some sort of nginx proxy. Either way, we have to do this manually since this proxying 
must exist before kubectl is operational. 

## Cluster Helm chart

This will basically all the extra stuff we need to add to the cluster to make it feel like a cloud
environment. For instance,
  - install the dynamic nfs volume provisioner on the cluster
  - install MetalLB on cluster

## Configure Monitoring

we should collect data on:
    - load times
    - which images are being used
    - cpu, memory, and data usage. Per user also.
    - also, all the kubernetes stuff, like pods per node and stuff.

maybe use prometheus? check this [blog post](
https://akomljen.com/get-kubernetes-cluster-metrics-with-prometheus-in-5-minutes/)

## Testing

We need an automated testing framework where we can put in test to simulate a bunch of users.
Maybe this could be cool: http://jmeter.apache.org/
But we need to do more complicated things, like have the clients run
programs or make graphs.

Yuvi mentioned this and that they had a way to do so, so we should contact him when we are ready.

We also test the cluster under failure by bringing down nodes and seeing how the cluster responds

## Publicity

Once we have something fully deployed, we should put our work on the binderhub
site under the [deployments section](https://binderhub.readthedocs.io/en/latest/known-deployments.html)
becuase it says they are looking for more people to post their deployments on there.



# Networking

Here is our basic setup for the nodes (not pods yet): ![our networking setup basically](../images/network.svg)
(taken from LibreTexts/Documentation/network_drawing as a saved svg)

## k8s network (internal network)

This is how all the computers will communicate with each other using kubernetes and how they will
access the internet indirectly though the manager. The manager will be a load balancer, dhcp server,
router with NAT, and our way assign IP addresses to services.

blue ethernet cables. Plugged into the smart switch.

manager is at 128.120.136.26

enp1s0 on all the machines (the one on the left but not the far left) except
the manager has it on enp3s0 which is the one as shown in the diagram above.

log into the switch with `screen /dev/ttyS0` on the management node
  - use username: manager
        password: friend
        

## Pod Network

This is the network so pods can communicate with each other. These will be running over
the k8s network

We meet the k8s [Network Policy](
https://kubernetes.io/docs/concepts/services-networking/network-policies/)
using Calico because it is faster than flannel. Alternatively, we could do it by hand
like is done in [k8s the hard way](
https://github.com/kelseyhightower/kubernetes-the-hard-way/blob/master/docs/11-pod-network-routes.md)


Using a pod CIDR of 10.244.0.0/16

Choosing calico. The manifest is in the home directory of the repo `calico.yaml`.
In this we changed:

    CALICO_IPV4_IPIP: "Never"
    CALICO_IPV4POOL_CIDER: "10.244.0.0/16"


## Management Network

We will have one management node and one dumb switch for this network. The management node
will connect to it on its enp2s0(the ethernet port on the right) and its management
interface (the one all the way to the left next to the usb ports).
It will run a DHCP server on this network.
The rest of the nodes will connect to this dumb switch only on their management interface.

Use green ethernet cables.

# Netbooting

otp on the manager node

follwing a combo of mostly this:
https://wiki.debian.org/PXEBootInstall#Preface
and also
https://help.ubuntu.com/18.04/installation-guide/amd64/ch04s05.html
and a little bit of
https://linuxhint.com/pxe_boot_ubuntu_server/


Using `10.0.0.0/24` for all the node IPs (chicks) so we have the manager as the
dhcp server also at `10.0.0.1`.

### quick word on hardaware

  network booting seems to work only on the enp1s0 interface on nodes. This is
  currently the one on the left. You cannot boot on the management interface
  that is located on the far left of the machines. Furthermore, this didn't work
  initially on the smart switch, so you must make sure that there are not routes
  or something already configured that would cause unexpected behavior. You also
  need to make sure you are doing this on a private network where the manager is
  the only dhcp server.
  After they were initially booted, I was able to switch them all over to the
  smart switch and there were no problems.

### steps on rooster (i.e. commands to run on rooster to get netboot to work):

1. `sudo apt install isc-dhcp-server`

1. to `/etc/default/isc-dhcp-server` I added the line:

    INTERFACESv4="enp3s0"

  since enp3s0 is the interface that is hooked up to the management network.
  Here, we assume enp3s0 is the interface on the manager node that faces the
  internal kubernetes network.

1. to `/etc/netplan/01-netcfg.yaml`, or whatever the netplan file is I added
  the following under ethernets:
    
              enp3s0:
                  addresses: [192.168.0.1/24]
                  gateway4: 128.120.136.1
                  dhcp4: no
                  nameservers:
                          addresses: [192.168.0.1]
    
  so we get that management interface up

1. `netplan apply`

1. before changing `/etc/dhcp/dhcpd.conf` copy the current one to
  `/etc/dhcp/dhcpd.conf.backup` and set it to this
  ```conf
# the following is adapted from
# https://wiki.debian.org/PXEBootInstall#Preface
#
default-lease-time 600;
max-lease-time 7200;

allow booting;
allow bootp;

# in this example, we serve DHCP requests from 10.0.0.(3 to 253)
# and we have a router at 10.0.0.1
# these will be the name of the nodes.
subnet 10.0.0.0 netmask 255.255.255.0 {
  range 10.0.0.3 10.0.0.99; # can't have 10.0.0.100 - 10.0.0.110 because we are
                            # using those for the chicks
  option broadcast-address 10.0.0.255;
  option routers 10.0.0.1;     # this ends up being the default gateway router
                               # on the hosts. Set to the manager so we can NAT
  option domain-name-servers 128.120.136.129,128.120.136.133,128.120.136.134;
  filename "pxelinux.0";
}

group {
  next-server 10.0.0.1;                # our Server. was previously 128.120.136.1
  host tftpclient {
    filename "pxelinux.0"; # (this we will provide later)
  }
}

  ```

1. `systemctl restart isc-dhcp-server` to get the dhcp server making
  repsjournalctl -fu isc-dhcp-server

1. checked the logs with `grep DHCP /var/log/syslog` and there were some
  requests and handouts, so thats good.

1. `sudo apt install tftpd-hpa`

1. changed `/etc/default/tftpd-hpa` to have these two defaults:
  ```
  TFTP_DIRECTORY="/srv/tftp"
  TFTP_OPTIONS="--secure -vvv"
  ```
  so we listen on our management net and not on the internet.
     ^- changed this, need to change it back after testing

1. `sudo mkdir /srv/tftp`

1. `systemctl restart tftpd-hpa` and then test it

1. `wget http://archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/current/images/netboot/netboot.tar.gz`

1. move netboot.tar.gz into `/srv/tftp` and run `tar xvzf netboot.tar.gz` and make the contents readable with `chmod -R a+r *`

1. `systemctl restart tftpd-hpa`

1. start up the client machine and it should get to a boot screen.

### configure NAT

1. `apt get ufw`

1. add the following to `/etc/ufw/before.rules`

```
    *nat
    :POSTROUTING ACCEPT [0:0]
    # send stuff out of the eth2 iface
    -A POSTROUTING -o enp2s0 -j MASQUERADE
    COMMIT
```

  note that enp2s0 is the interface that faces the public internet

1. uncomment `net/ipv4/ip_forward=1` in `/etc/ufw/sysctl.conf`

1. `systemctl restart ufw`

1. `sudo ufw allow tftp` so it can use the images


### steps on chicks (i.e. things you need to do to boot a node on the network)

1. have it connected to enp1s0 which is the left ethernet port on the right side

1. power it on with the disks in. The install screen should come on. If not, you
  may have to change the boot priority order

1. go through the installation steps. Once it says "installing base system,"
  that part takes like an hour so you can go do something else. After that its
  mostly done. Alternatively, you could use the preseed file to  
  install the OS onto each chick with very little intervention. Check the next section
  on how to go about this.

1. after completing the installation, to get it to boot from disk, you have to
  turn off the network boot on the manager (rooster). So on rooster, run
  `systemctl stop tftpd-hpa` before rebooting your newly installed machine.
  After it boots, you can turn tftp back on.
  
#### Alternative route: preseeding
With preseeding, you can install Ubuntu Server 18.04 using a preconfiguration file,
without going through each installation step manually.

The preconfiguration file is located in the tftp server: `/srv/tftp/pxelinux.cfg/default`.
Under `label cli` lists the tasks and boot parameters needed to automate most of the
configuration.

The file `srv/tftp/preseed.cfg` lists the preconfiguration options. We removed the
partitioning section of the preconfiguration file because we wanted to keep the 
RAID arrays already in place of each chick.

In order to use preseeding, type in the command `cli` after the `boot:` prompt when pxelinux
shows up from booting from the network.

In `/etc/dhcp/dhcpd.conf`, to each host, add `option host-name "<HOSTNAME>";` 
to each host. This is for dhcp to replace the hostname of the computer. Alternatively,
you could type in `cli hostname=<HOSTNAME>` when booting each chick.

# Adding Nodes

First, check out [Netbooting](#Netbooting) to get the OS installed.
This section will cover what you have to do to get the
node functioning in the kubernetes cluster after the os is already installed.

1. figure out the ip address that was assigned by the manager's dhcp server by
  checking out the logs on rooster. Logs are in `/var/log/syslog` for dhcp, so
  run something like `grep dhcp /var/log/syslog` and there will be mention of
  what ip it was assigned.

1. Add the node to `chicks.csv` by manually adding the hostname and the ip address
  and other fields. Then, on rooster run `./get_macs.py`
  and this will automatically fill in the `enp1s0` and `enp2s0` fields with the
  mac address on those interfaces. See the comments at `get_macs.py`.

1. Optionally assign a static ip address to the host by changing
  `/etc/dhcp/dhcpd.conf` on the master and adding the mac address and the ip
  address you want. See the comments and other examples in that file.
  Then run `systemctl restart isc-dhcp-server`. It will
  take a little while for the node's current ip lease to expire and for it to
  recieve the new IP, or you can run `netplan apply` and the host will reload
  its ip info from the router.

1. Add it to the `hosts` file under the ansible directory.

1. Provision all of them using the ansible playbook. From the `ansible/`
  directory, run `anisble-playbook -i hosts playbooks/main.yml --ask-become-pass`.
  You sometimes have to change it to `--ask-pass` and change it back. I dont know why.
  It might be a bug. If you are
  just adding one host and not provisioning the whole cluster, add the `--limit "chick{i}`
  flag.
 
## Adding Individual Nodes
  
If you are adding a completely new node, add the `--limit "chick{i}` flag, 
then run the playbook `workers.yml` with both the master and new chick node. 
  
The first task will give you a fatal error for the task, `join cluster`; this
is expected. (We can probably write another playbook for adding nodes, but would involve
a lot of copying and pasting.)
```
ansible-playbook -i hosts playbooks/main.yml --ask-become-pass --limit "chick{i}"
ansible-playbook -i hosts playbooks/workers.yml --ask-become-pass --limit "chick{i},master"
```
If you are adding a wiped node whose name is still in the cluster, i.e. the name of
the node still appears when running `kubectl get nodes`, then delete the node first
by running `kubectl delete node <node-name>` and completely wipe the node again.
Then follow the steps as if you were adding a completely new node.
  
If you are adding a node that has been detached (e.g. you restarted the system
on the node), then run `sudo systemctl restart kubelet.service`. If you still have
trouble, this may help: [Troubleshooting](https://github.com/libretexts/metalc/docs/BareMetalTroubleshooting/AddingNotReadyNode.md)

# Publishing Services

These are notes about how services of type `LoadBalancer` will be handled on our cluster.

## Metallb

[MetalLB](https://metallb.universe.tf) is a way to assign IPs to services from
a pool of IP addresses.

Config is at `metallb-config.yml` in the root of the project.

CELINE: we probably need to add a play in the ansible playbook on the master
group so it can [install metallb](https://metallb.universe.tf/installation/)
and also run `kubectl apply metallb-config.yml` for the config.

our pool of public ips open on ports 80 and 443 are as follows:

    128.120.136.32
    128.120.136.54
    128.120.136.55
    128.120.136.56
    128.120.136.61

## Notes on Layer 2

We must use the layer 2 for metallb because calico is already using BGP to
communicate its own routes. This problem is talked about [here](
https://metallb.universe.tf/configuration/calico/).

We still have a problem with getting IPs requests for any of the above public IPs
forwarded through the manager node and to our switch. (once it gets to the switch,
it should be fine since within this network, the ip will be correctly assigned with
ARP by metalc).

## Possible Solutions

### Plug all the chicks into the 128.120.136 network

The problem with this is that we need dhcp within this cluster and are running
netboot on this network. So it might be best for it to be on an alternate interface
and maybe we could do that later.

### Have a separate set of "public ips"

In this solution, each public IP above has a corresponding IP within the k8s
network so that the manager can accept requests on the public network for all
of the above public IPs and then forward them to the corresponding k8s "public"
ip on the internal k8s network. Then MetalLB will use these internal k8s "public"
ips to assign to services. This will allow the services to be publicly accessible.

This is the solution currently implemented and it works right now.

We have `128.120.136.{i}` forward to `10.0.1.{i}` internally.

On rooster, we listen on the public
network for all of the above public IPs. This is done by modifying
`/etc/netplan/01-netcrg.yaml` as follows:


          # public network
          enp2s0:
                  addresses:
                   # IP assigned for rooster
                          - 128.120.136.26/24

                   # public ips that richard gave us to publish services
                          - 128.120.136.32/24
                          - 128.120.136.54/24
                          - 128.120.136.55/24
                          - 128.120.136.56/24
                          - 128.120.136.61/24
                  gateway4: 128.120.136.1
                  dhcp4: no
                  nameservers:
                          addresses: [128.120.136.129,128.120.136.133,128.120.136.134]

Apply the netplan configuration by running `sudo netplan apply`.

Then for the forwarding, we use nginx and forward from public to private. The following
is part of `/etc/nginx/nginx.conf` forwarding:

```

# this is where we forward to the "public" ips internally
# only did the first 3. 
	server {
		listen 128.120.136.32;

		location / {
			proxy_pass http://10.0.1.32;

			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header Host $host;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-NginX-Proxy true;
		}
	}

	server {
		listen 128.120.136.54;

		location / {
			proxy_pass http://10.0.1.54;

			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header Host $host;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-NginX-Proxy true;
		}
	}

```

Apply the nginx configuration by running `systemctl restart nginx.service`.

Finally, on `metallb-config.yml` the pool of IPs are the internal "public" ips
beginning with `10.0.1.`.

Add the IP addresses to `metallb-config.yml` and run `kubectl apply -f metallb-config.yml`.


## NFS
NFS is needed to handle persistent volume claims. It allows persistence of files made by
the nodes.

(Credit to [Kevin's kube-dev-env](https://github.com/kkrausse/kube-dev-env))

In rooster, run `sudo apt install nfs-kernel-server` to install the NFS server on the
host system. We will use `/export` on rooster as the shared directory which the chicks 
can access.

Add the following line to `/etc/exports`:
```
/export 10.0.0.0/8(rw,fsid=0,async,no_subtree_check,no_auth_nlm,insecure,no_root_squash)
```
and run `exportfs -a`.

To make sure the NFS mount is successful, run this command on rooster to allow anything 
from the network of chicks to talk to rooster: `ufw allow from 10.0.0.0/8 to 10.0.0.1`.
Without this command, the firewall won't allow you to mount NFS.

We want each chick to mount `10.0.0.1:/export` (on rooster) to `/nfs` (locally on the chick
node). The Ansible Playbook already auto-mounts rooster to each chick by editing the
`/etc/fstab` file, so you don't have to do this manually. If you do want to do it manually, 
run the command `sudo mount 10.0.0.1:/export /nfs` on each chick node.

The `nfs-client-vals.yml` describes the values used for running the NFS client provisioner.
Run
```
helm install --name nfs-client-release stable/nfs-client-provisioner -f nfs-client-vals.yml
```

Then follow [these instructions](https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-helm.html)
for setting up JupyterHub.

Later, we will have a physical NFS server.

# Accessing the Cluster
Ssh into rooster on putty.
On putty, click the upper left, go to **Change Settings**. In the left menu, go to **SSH**, then **Tunnels** 
to add a new port forwarding rule.
For **Source port**, type `4545`.
Select `Dynamic`. Click **Add**.

In Mozilla Firefox, go to **Tools**, then **Options**.
Under **Network Settings**, click **Settings**.
Select **Manual proxy configuration**. In SOCKS Host, enter `localhost`. In Port, enter `4545`. Select **SOCKSv4**.

Now, open http://10.0.1.54.

# Literature List

Place for us to add some useful reading we find

### General Kubernetes

Obviously, the [concepts section](https://kubernetes.io/docs/concepts/) is
probably the most valueable resource for learning about kubernetes. Services,
Load Balancing, and networking is probably the most important aspect for our
intents and purposes. Also, check out the [/dev-env](https://github.com/LibreTexts/metalc/tree/master/dev-env)
to give yourself a kubernetes cluster to mess with while learning.

good intro blog on basics like containers and kubernetes: [what is a kubelet](http://kamalmarhubi.com/blog/2015/08/27/what-even-is-a-kubelet/)

Building a Kubernetes cluster using Ansible Playbooks: [How to Build a Kubernetes Cluster Using Kubeadm on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-create-a-kubernetes-cluster-using-kubeadm-on-ubuntu-18-04)

### Networking
Introduction to ports and IP addresses: [TCP/IP Ports and Sockets Explained](http://www.steves-internet-guide.com/tcpip-ports-sockets/)

Some info on NFS server setup: [Install NFS Server and Client on Ubuntu 18.04](https://vitux.com/install-nfs-server-and-client-on-ubuntu/)

More on NFS: [How to Set Up an NFS Mount](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-18-04)

### Installation
A post about pxelinux.cfg file setup for unattended installs of Ubuntu 18.04: [Ubuntu 18.04 Unattended Setup](https://opstuff.blog/2018/10/16/ubuntu-18-04-unattended-setup/)


### Reference Repositories
[NFS Client Provisioner](https://github.com/helm/charts/tree/master/stable/nfs-client-provisioner)
for setting up an automatic provisioner after you have the NFS server set up.

# Useful Commands
* `kubectl get service` lists the services of the clusters, with cluster IP, external IP, and ports.
* `kubectl get po -A` lists all pods in the cluster.
* `tail /var/log/syslog` gives the latest updates on dhcp, ufw, etc.