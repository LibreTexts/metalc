# Restoring Kubernetes Objects

## Problem

We just moved the cluster. In doing so, all of the previous Kubernetes objects (most of which do not matter, but the PV/PVCs do!) were wiped! Here are some steps that may help in trying to restore the Kubernetes objects.

### Context

In our cluster, Kubernetes objects are stored in key-value pairs in etcd. This data is stored on any control plane nodes and is served through etcd pods. Interacting with etcd is the key to restoring this data.

### Prerequisites

Of course, in order to restore the data, the data must be somewhere. In our situation we had:
- The old cluster, which had all of the data but was non-functioning.
- The new cluster, which had none of the data and only one control plane node.

Even though the old cluster did not have a management node, the actual etcd pod itself was still running. Thus, at least in order to get the old data, an etcd pod must be running. This could of course be avoided by just getting the data before shutting anything down just in case.

## Solution

### Getting the old data

To get the old data, we get what's called an etcd snapshot. We have to get into the etcd pod to do so. Without access to kubectl, we could do this by going on to any control plane node and performing the following steps:

Run `sudo crictl ps`<sup>1</sup> to find the etcd process. Take note of the container ID.

Then run<sup>2</sup>

```
sudo crictl exec -it {CONTAINER_ID} etcdctl --cacert=/etc/Kubernetes/pki/etcd/ca.crt --cert=/etc/Kubernetes/pki/etcd/server.crt –-key=/etc/Kubernetes/pki/etcd/server.key snapshot save /var/lib/etcd/snapshot.db
```

Where `{CONTAINER_ID}` is the container ID noted earlier. This will save a snapshot in `/var/lib/etcd/snapshot.db`, which is accessible from the node.

Now copy the snapshot file from its location to somewhere more accessible, like perhaps `~`. Move this file onto the target node with whichever method is most convenient (like SCP).

### Restoring from the old data

At this point, we should have a `snapshot.db` from the old cluster/node on the new node somewhere accessible.

Move this file into `/var/lib/etcd` so it is accessible to etcd.

Similar to the obtaining process, run `sudo crictl ps` to find the container ID of the pod that is running etcd on the node.

Now run

```
sudo crictl exec -it {CONTAINER_ID} etcdctl --cacert=/etc/Kubernetes/pki/etcd/ca.crt --cert=/etc/Kubernetes/pki/etcd/server.crt –-key=/etc/Kubernetes/pki/etcd/server.key snapshot restore /var/lib/etcd/snapshot.db
```

Note how similar this command is to the one we ran to save the data to the snapshot.

Now the unpacked data will be in `/default.etcd`. We need to move it into the place where it actually gets used. Unfortunately, this directly is not so easily accessible from the node.

Run `sudo mount | grep {CONTAINER_ID}`<sup>3</sup> to find possible snapshot directories where this particular directory will be.

Once found, copy the data into an accessible directory temporarily. For example:

`sudo cp -r /var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/1157/fs/default.etcd/member ./`

Now we want to clear any leftover etcd data that may be there. We do this by running `sudo rm -r /var/lib/etcd/member`.

Then we put the restored data into the directory we just cleared. For example:

`sudo cp -r member/ /var/lib/etcd/`

Messing with the etcd data while the pod is running may restart it. This is normal.

At this point, the data should be restored.

### Footnotes

1: `crictl` is a utility to interface with containerd, which is the backend for containers.

2: This command will execute the command following the container ID inside of said container. `etcdctl` is the utility to interface with etcd. We are telling it to save a snapshot. We have to give it some Kubernetes specific certs to work properly. These certs are fixed and will always be in the specified locations in a typical Kubernetes cluster.

3: Running mount shows us all of the active mounts on the system. We want to know which mounts are associated with the etcd container, so we grep with its ID.
