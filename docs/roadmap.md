# Cluster Roadmap

Basically, a todo list for the cluster

# Minimum Requirements

## On-Premis Requirements

This is stuff that needs to be done before all work can be done remotely.

- rack all servers and nfs server (remember to put RAM in all servers)
- put disks in the servers
- install OS (can only be done after disks are in)
- wiring for the networking
- networking -- though this technically can be done remotely, we might break
  something while doing it so we should do it on-premis.
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
failing. The setup is outlined in the [kubeadm docs](
The https://kubernetes.io/docs/setup/independent/high-availability/). We can use either [HA proxy](
http://www.haproxy.org/#desc), which Richard is familiar with, or maybe some sort of nginx proxy. Either
way, we have to do this manually since this proxying must exist before kubectl is operational. 

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
