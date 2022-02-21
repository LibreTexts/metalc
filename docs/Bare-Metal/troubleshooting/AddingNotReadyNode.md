# How to re-add a node to the cluster after manually shutting it down

## Error code: 255
I rebooted chick9 and `kubectl get nodes` revealed:
```
NAME      STATUS     ROLES    AGE    VERSION
chick0    Ready      master   5d1h   v1.14.0
chick1    Ready      <none>   5d1h   v1.14.0
chick2    Ready      <none>   5d1h   v1.14.0
chick3    Ready      <none>   5d1h   v1.14.0
chick4    Ready      <none>   5d1h   v1.14.0
chick5    Ready      <none>   5d1h   v1.14.0
chick6    Ready      <none>   5d1h   v1.14.0
chick7    Ready      <none>   5d1h   v1.14.0
chick8    Ready      <none>   5d1h   v1.14.0
chick9    NotReady   <none>   5d1h   v1.14.0
```

## Potential Solution
The trouble shooting section of [this documentation](https://opensource.ncsa.illinois.edu/confluence/display/~lambert8/Kubernetes)
revealed that the `kubelet` service should be restarted to 
add chick9 back into the cluster.

First, ssh into the node with the NotReady state by running `ssh chick<NUMBER>`.
Running `sudo systemctl restart kubelet.service` and checking the status with
`systemctl status kubelet.service` returns an error code: 255.

Check if the node is added by running `kubectl get nodes`.

In my case, chick9 was still `NotReady`. Checking the logs with `journalctl --since <time>` 
revealed that swap needed to be disabled for kubelet to run.

```
Jun 17 14:00:00 chick9 kubelet[18280]...failed to run Kubelet: Running with swap on is not supported, please disable swap!
```

Disable swap by running `sudo swapoff -a`.
Check if the node is active by running `systemctl status kubelet.service`.

Exit ssh and run `kubectl get nodes` to check the status of your node.

## Another Potential Solution
It may be the case that kubelet is trying to use the default docker daemon instead of the containerd one.

Modify `/var/lib/kubelet/kubeadm-flags.env` to read `KUBELET_KUBEADM_ARGS="--container-runtime=remote --container-runtime-endpoint=/run/containerd/containerd.sock"`, then restart kubelet.

## Rejoining from fresh install
Puppet will want the node to join the cluster immediately. However, it may not be able to immediately due to several possible issues.

Firstly, `sudo puppet agent -t --debug` will start a puppet run with a lot of extra debugging features. 
Always use this to figure out what is going on.

In order for nodes to communicate with the puppet master, it will require correct certificates. 
`sudo puppet node clean {node name}.galaxy` will clear old certificates.

Kubernetes also needs tokens to have nodes join the cluster. On a nebula node, one can run 
`sudo kubeadm token create galaxy.bab852737673e5a4 --v=5` to generate a new token for the node to use.
