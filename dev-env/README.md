## Running

taken some from:
https://www.digitalocean.com/community/tutorials/how-to-create-a-kubernetes-cluster-using-kubeadm-on-ubuntu-18-04

also a good one:
https://blog.laputa.io/kubernetes-flannel-networking-6a1cb1f8ec7c

### Step 1: Install prerequisites

- Install Vagrant, VirtualBox, kubectl, Ansible, and [Helm](
https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-helm.html)
you have to do the last one yourself, but you can copy/paste this:

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl

sudo apt-get install virtualbox
sudo apt-get install vagrant
sudo apt install ansible
```

### Step 2: Set up network

- Since Vagrant with VirtualBox failed to set up a private network, I will
  do this manually by running the following:
```
# add a tap interface to connect all nodes in the network and name it tap0
# all the vms will create a bridge to this interface and thus be connected
# the name "tap0" is important since its used in the vagrantfile
sudo ip tuntap add name tap0 mode tap
# set the ip that the host will use for the tap interface
sudo ip addr add 192.168.99.1 dev tap0
# put the tap interface up
sudo ip link set dev tap0 up
# configure your ip to route requests to this interface
sudo ip route add 192.168.99.0/24 dev tap0
```

To verify you have set up the tap interface, you can run the command `route`. 
You should see an additional entry in your Kernel IP routing table:
```
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
192.168.99.0    0.0.0.0         255.255.255.0   U     0      0        0 tap0
```

### Step 3: Set up cluster

If you have not already, clone this repository.
Open `Vagrantfile` and set the variable `N` to the number of worker nodes you want

Run `vagrant up` to set up the nodes and then `vagrant provision` to set up
the kubernetes cluster. This uses the Ansible Playbooks to configure all the
nodes.

### Step 4: Interracting with the cluster

To make things easier, you can set the node names in your `/etc/hosts` file.
I added the following lines:
```
192.168.99.20 node0.test.com node0
192.168.99.21 node1.test.com node1
192.168.99.22 node2.test.com node2
```

You can run kubectl by sshing into the master (`ssh ubuntu@node0`) or you can
run it on the host machine by copying the kubernetes config file and putting it
in a readable location.

Run `scp ubuntu@node0:/home/ubuntu/.kube/config .` to copy the config to your
current directory and then run `export KUBECONFIG="$(pwd)/config"` so kubectl
knows to operate on this config.

Alternatively, you can just place the `config` file in your `~/.kube/` directory

Run `kubectl get nodes` to see that all your nodes are ready to roll

### Step 5(optional): Add default storage class

This will make it so persistant volume claims are automatically satisfied by
[dynamically provisioned](
https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/) persistent
volumes. You dont have to do this step, but if any deployment creates a
Persistent Volume Claim, you will have to provision a persistent volume
manually to satisfy the claim.

In this case, I am running an nfs server on the host and using the [nfs client](
https://github.com/helm/charts/tree/master/stable/nfs-client-provisioner)
as an external provisioner. You can run the nfs server on any machine though.
Just replace `192.168.99.1` with the ip address of the host that you are running
the nfs server on and make sure all the nodes can access it.

##### Running NFS on the host OS

Run `sudo apt install nfs-kernel-server` to run the nfs server on the host and
add the following line to `/etc/exports`:
```
/path/to/shared/directory *(rw,fsid=0,async,no_subtree_check,no_auth_nlm,insecure,no_root_squash)
```
where `/path/to/shared/directory` will be the directory you will share over nfs.
nfs-client-provisioner will created a directory within this directory for every
volume that it provisions.

Then `sudo exportfs -a` to update the nfs server.

lastly, `chmod -rw /path/to/shared/directory` so kubernetes can alter it.

##### Setting up the NFS client external provisioner

While in the root directory of this repository, run
```
helm install --name nfs-client-release stable/nfs-client-provisioner -f nfs-client-vals.yml 
```

For reference this helm chart is based on this [repo](https://github.com/kubernetes-incubator/external-storage/tree/master/nfs-client).
Code in `nfs-client/cmd/nfs-client-provisioner` implements the kubernetes volume provisioner [interface](
https://github.com/kubernetes-sigs/sig-storage-lib-external-provisioner/blob/master/controller/volume.go)
and the helm chart has a deployment that makes a pod that runs this one file
and creates a storage class that uses the provisioner.

Delete the nfs client provisioner with:
```
helm delete nfs-client-release --purge
```

### Done

You should now be able to run the jupyterhub [Helm chart](
https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-jupyterhub.html) on this cluster

#### Exposing JupyterHub
One way to publicly expose JupyterHub: forward requests using an upstream block.
First, find the IP address of the node that JupyterHub is running on.
```
$ kubectl get pods -n jhub
NAME                                                       READY   STATUS    RESTARTS   AGE
hub-5c458869b6-q9mjz                                       1/1     Running   0          3h29m
nfs-client-release-nfs-client-provisioner-9c489f48-5b7k9   1/1     Running   5          55d
proxy-ddc67f979-4rlqs                                      1/1     Running   0          3d5h

$ kubectl describe pod hub-5c458869b6-q9mjz -n jhub
...
Node:               node2/192.168.99.22
...
```
We know that JupyterHub is running on node2, which has the IP of 192.168.99.22.

```
$ kubectl get svc -n jhub
NAME           TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
hub            ClusterIP      10.104.64.184   <none>        8081/TCP                     55d
proxy-api      ClusterIP      10.104.232.54   <none>        8001/TCP                     55d
proxy-public   LoadBalancer   10.97.147.113   <pending>     80:32335/TCP,443:32667/TCP   55d
```
We also know that the LoadBalancer is exposed on port 32335 of node2.

In `/etc/nginx/nginx.conf`, we can add this to the `http` and `server` blocks:
```
...
http {
    upstream root_host {
        server 192.168.99.22:32335;
    }
...

server {
    listen 443;
    server_name <your domain>
    
    location / {
      proxy_pass http://root_host;
      ...
    }
  }
...
}   
```
This is assuming that you have run Let's Encrypt/Certbot on your server.
Use `sudo nginx -t` to make sure the syntax is correct and `systemctl restart nginx.service`
to restart nginx. JupyterHub should now be live on your domain!

### Tearing it down
To delete the virtual machines and cluster, run
```
vagrant destroy -f node2
vagrant destroy -f node1
vagrant destroy -f node0
```

### Vocabulary

- when I say "host machine," I am talking about the machine that vagrant and
  and virtual box are installed on. This is opposed to "guest machine" which
  is one that is virtual.
