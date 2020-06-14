# Connection to the server 10.0.0.100:6443 was refused: Possible Solutions

## Problem
Running any `kubectl` command on rooster gave an error.
```
$ kubectl get nodes
The connection to the server 10.0.0.100:6443 was refused - did you specify the right host or port?
```

JupyterHub went down. Surprisingly, Grafana was still accessible (but didn't give
any alerts).

## Most Common Solution: Disabling Swap
Nodes restart on their own sometimes (due to various causes, such as hardware,
high memory use, etc.). On reboot, they may end up enabling swap.

This is a [fairly common problem](https://discuss.kubernetes.io/t/the-connection-to-the-server-host-6443-was-refused-did-you-specify-the-right-host-or-port/552/5).
You must [disable swap to use Kubernetes](https://serverfault.com/questions/881517/why-disable-swap-on-kubernetes).

> Why? When a computer runs out of physical memory, it uses virtual memory, which
means that the data starts going to the hard disk. However, accessing the 
hard disk is **much** slower than accessing memory. Kubernetes assumes that
however much memory is "available" is physical memory, not including swap.
[More information here](https://serverfault.com/questions/881517/why-disable-swap-on-kubernetes).

SSH into the master node, `chick0`. Disable swap and restart kubelet.  
```
$ ssh chick0
$ sudo swapoff -a
$ sudo systemctl restart kubelet
```
Ensure kubelet is active by running `sudo systemctl status kubelet`.

For a more permanent solution, open `/etc/fstab` and comment out the line 
which starts with `/swapfile`. (We have a [task for this in Ansible](https://github.com/LibreTexts/metalc/blob/86ec49d757c44dcc0bca785c9175f429c9d79718/ansible/playbooks/kube-deps.yml#L64).)

Note: this is a similar solution to [AddingNotReadyNode.md](./AddingNotReadyNode.md).


## More Complex Solution: Renewing Kubeadm Certificates
Unfortunately, even after disabling swap, kubelet may refuse to restart.

Running `sudo systemctl status kubelet` showed that kubelet was not active
and gave a pretty nondescript error.

Turning to the logs inside chick0 gave a more descriptive problem.
```
$ journalctl -u kubelet -r
Jun 11 16:06:19 chick0 kubelet[30057]: F0611 16:06:19.164887   30057 server.go:271] failed to run Kubelet: unable to load bootstrap kubeconfig: stat /etc/kubernetes/bootstrap-kubelet.conf: no such file or directory
Jun 11 16:06:19 chick0 kubelet[30057]: E0611 16:06:19.164838   30057 bootstrap.go:265] part of the existing bootstrap client certificate is expired: 2020-06-11 20:11:55 +0000 UTC
```

> Note: `journalctl -u kubelet -r`: the `-u` indicates which program you want
to get logs from, and `-r` means you want to look a the logs from the most
recent to oldest.

Interestingly, the file `/etc/kubernetes/bootstrap-kubelet.conf` doesn't exist.
Even after solving the problem, it still doesn't exist. My theory is that
it tried to look for that file after encountering an expired certificate.

We checked the expiration status of the certificates, and it turns out they 
were all expired! Turns out that the kubeadm certificates expire in 1 year
by default. 

"We celebrate the one-year anniversary of our cluster by it going
down."
* [kubeadm alpha certs check-expiration documentation](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-alpha/#cmd-certs-check-expiration)
```
$ sudo kubeadm alpha certs check-expiration
CERTIFICATE                EXPIRES                  RESIDUAL TIME EXTERNALLY MANAGED
admin.conf                 Jun 11, 2020 23:52 UTC   0d            no
apiserver                  Jun 11, 2020 23:52 UTC   0d            no
apiserver-etcd-client      Jun 11, 2020 23:52 UTC   0d            no
apiserver-kubelet-client   Jun 11, 2020 23:52 UTC   0d            no
controller-manager.conf    Jun 11, 2020 23:52 UTC   0d            no
etcd-healthcheck-client    Jun 11, 2020 23:52 UTC   0d            no
etcd-peer                  Jun 11, 2020 23:52 UTC   0d            no
etcd-server                Jun 11, 2020 23:52 UTC   0d            no
front-proxy-client         Jun 11, 2020 23:52 UTC   0d            no
scheduler.conf             Jun 11, 2020 23:52 UTC   0d            no
```

We suggest backing up the configuration files and certificates before proceeding.
The following command copies the Kubernetes configurations directory
to the home directory.
```
$ sudo cp -r /etc/kubernetes/ ~/
```

[Renew all the certificates](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-alpha/#cmd-certs-renew). Note that this replaces the configuration
files in `/etc/kubernetes`.
```
$ sudo kubeadm alpha certs renew all
$ sudo kubeadm alpha certs check-expiration
CERTIFICATE                EXPIRES                  RESIDUAL TIME   EXTERNALLY MANAGED
admin.conf                 Jun 11, 2021 23:52 UTC   364d            no
apiserver                  Jun 11, 2021 23:52 UTC   364d            no
apiserver-etcd-client      Jun 11, 2021 23:52 UTC   364d            no
apiserver-kubelet-client   Jun 11, 2021 23:52 UTC   364d            no
controller-manager.conf    Jun 11, 2021 23:52 UTC   364d            no
etcd-healthcheck-client    Jun 11, 2021 23:52 UTC   364d            no
etcd-peer                  Jun 11, 2021 23:52 UTC   364d            no
etcd-server                Jun 11, 2021 23:52 UTC   364d            no
front-proxy-client         Jun 11, 2021 23:52 UTC   364d            no
scheduler.conf             Jun 11, 2021 23:52 UTC   364d            no
```

Note that this renews the certificates for all configurations in `/etc/kubernetes`
*except for* `/etc/kubernetes/kubelet.conf`. 
[Renew the certificate](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-kubeconfig) 
for `kubelet.conf`.
```
$ sudo kubeadm init phase kubeconfig kubelet --apiserver-advertise-address 10.0.0.100 --node-name chick0
```

> [More info on kubeadm implementation](https://kubernetes.io/docs/reference/setup-tools/kubeadm/implementation-details/). 

Kubelet is now active (you can see the Docker containers running 
with `sudo docker ps`!). Running `kubectl` gives an error though.
```
$ kubectl get nodes
error: error loading config file "/home/spicy/.kube/config": open /home/spicy/.kube/config: permission denied
```
The environment 
variable `KUBECONFIG` is set to `~/.kube/config`, which was the previous 
copy of `/etc/kubernetes/admin.conf` before we renewed the certificates. 

Update this by either setting `KUBECONFIG` to `/etc/kubernetes/admin.conf` or
copying the updated `admin.conf` to `config`. 
[Slightly related instructions here](https://discuss.kubernetes.io/t/the-connection-to-the-server-host-6443-was-refused-did-you-specify-the-right-host-or-port/552/26).
```
$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
$ sudo systemctl restart kubelet
```

> Make sure that `~/.kube/config` has the same read-write permissions as the old
config file. You can run `ls -l` to compare. For example, we had to add read permissions.
  ```
  $ ls -l
  total 24
  drwxr-xr-x 3 spicy spicy 4096 Jun 12  2019 cache
  -rw------- 1 root  root  5446 Jun 11 18:37 config
  -rw-r--r-- 1 spicy spicy 5450 Jun 12  2019 config.backup
  drwxrwxr-x 3 spicy spicy 4096 Jun 11 18:38 http-cache
  $ sudo chmod +r config
  ```

Now, `kubectl` works on `chick0`, but not on rooster. Exit SSH from chick0 
and return to rooster. Back up the config and copy the updated config 
from chick0 to rooster. 
```
$ cp ~/.kube/config ~/.kube/config.backup
$ scp 10.0.0.100:/home/spicy/.kube/config ~/.kube/config 
```

Run `kubectl get nodes` to ensure that `kubectl` now works.

## Further notes
* [A GitHub comment with the manual way of renewing certificates](https://github.com/kubernetes/kubeadm/issues/581#issuecomment-421477139). We used this for guidance, but did not follow the instructions.
* Some commands online are outdated. For example, `sudo kubeadm alpha phase kubeconfig` is now `sudo kubeadm init phase kubeconfig`.
* [An attempted solution we did by removing a kubelet key symlink](https://github.com/kubernetes/kubernetes/issues/65991#issuecomment-486498651)
* [Potential solution](https://stackoverflow.com/questions/56320930/renew-kubernetes-pki-after-expired?noredirect=1&lq=1) on Stack Overflow
* [Pretty close to our solution](https://github.com/kubernetes/kubeadm/issues/1361) on GitHub
* [An overview on renewing certificates](https://reece.tech/posts/renewing-kubernetes-certificates/), but this involves you actually being able to use `kubectl`
* Happy 1st birthday to the flock cluster! :-) 
