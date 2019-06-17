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

## Solution
The trouble shooting section of [this documentation](https://opensource.ncsa.illinois.edu/confluence/display/~lambert8/Kubernetes)
revealed that the `kubelet` service should be restarted to 
add chick9 back into the cluster.

First, ssh into the node with the NotReady state by running `ssh chick<NUMBER>`.
Running `sudo systemctl restart kubelet.service` and checking the status with
`systemctl status kubelet.service` returns an error code: 255.

Checking the logs with `journalctl --since <time>` revealed that swap needed
to be disabled for kubelet to run.

```
Jun 17 14:00:00 chick9 kubelet[18280]...failed to run Kubelet: Running with swap on is not supported, please disable swap!
```

Disable swap by running `sudo swapoff -a`.
Check if the node is active by running `systemctl status kubelet.service`.

Exit ssh and run `kubectl get nodes` to check the status of your node.
