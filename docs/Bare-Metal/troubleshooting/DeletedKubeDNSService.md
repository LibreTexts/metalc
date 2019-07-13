# Restoring a Service
More specifically, the `kube-dns` service.
## Problem
I deleted the `kube-dns` service by the command `kubectl delete svc`. So, when running 
`kubectl get service -n kube-system` (aka the services under the namespace, kube-system),
this would result:
```
NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
tiller-deploy   ClusterIP   10.109.104.129   <none>        44134/TCP                24d
```
So unfortunately, the `kube-dns` service didn't pop up.
But, the core-dns pods were still running.
`kubectl get pods -A`:
```
NAMESPACE        NAME                                                        READY   STATUS    RESTARTS   AGE
kube-system      coredns-fb8b8dccf-7qxlh                                     1/1     Running   0          7d
kube-system      coredns-fb8b8dccf-hcfnt                                     1/1     Running   0          7d
```

## Solution
According to the docs for the 
[kubeadm init sequence](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#init-phases),
you could run a specific phase.

So I SSHed into chick0, the master and ran the sequence just for kube-dns.
```
ssh chick0
sudo kubeadm init phase addon coredns
```

In rooster, we could see that the kube-dns service is restored.
```
$ kubectl get service
NAME          TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes    ClusterIP      10.96.0.1       <none>        443/TCP        30d
nginx-spare   LoadBalancer   10.111.146.92   10.0.1.32     80:32124/TCP   27d
```

The `core-dns` pods are recently created, too. They seemed to replace the older ones?
```
$ kubectl get pods
coredns-fb8b8dccf-7qxlh                    1/1     Running   0          19m
coredns-fb8b8dccf-hcfnt                    1/1     Running   0          19m
```

I followed the verification steps [here](https://github.com/kelseyhightower/kubernetes-the-hard-way/blob/master/docs/12-dns-addon.md#verification)
to make sure everything was working.

More resources on `kube-dns`:
* [Deploying core-dns](https://linuxacademy.com/linux/training/lesson/course/kubernetes-the-hard-way/name/deploying-core-dns)
* [Kube-dns information on DigitalOcean](https://www.digitalocean.com/community/tutorials/an-introduction-to-the-kubernetes-dns-service)
* [Core-dns on Learning Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way/blob/master/docs/12-dns-addon.md)
