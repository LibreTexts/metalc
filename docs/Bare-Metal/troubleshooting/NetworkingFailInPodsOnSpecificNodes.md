# Networking fail in pods spawned on specific nodes

## Problem

On 2020-06-17, I upgraded most of the worker nodes using `apt upgrade`, which also bumped kubelet to version `1.16.10-00`. Not sure if this is relevant to the problem, but the issue began around then. After investigating some crashing pods, we found that some pods do not have DNS (the pod crashes because one of the initialization containers for staging-jhub tries to clone from github, and the logs for the failing initialization container [[1]](#investigating-crashing-logs-on-an-init-container) we found the error was "could not resolve host github.com").

After some hair pulling (and figuring out not _all_ pods have DNS broken), we found it might be node related. We created pods on some of the nodes [[2]](#2) and found that chicks 11 and 18 always have failing DNS while chicks 1 and 10 have working DNS. `/etc/resolv.conf` seem to show the right IP for kube-dns (10.96.0.10), but we can't even ping that IP in broken pods. When we investigated chick 11 more thoroughly, we found a bunch of errors in `systemctl`:

```
Jun 17 23:00:14 chick11 kubelet[780]: W0617 23:00:14.506148     780 docker_sandbox.go:394] failed to read pod IP from plugin/docker: networkPlugin cni failed on the status hook for pod "continuous-image-puller-vnxmz_binderhub": CNI failed to retrieve network namespace path: cannot find network namespace for the terminated container "b79ba7b1837fa949a58388afaa11f0b46807d55a2238f8964865132b6216853f"
```

Error messages like these were occuring around a dozen times a second, so something is messed up with the networking. Google brought me [here](https://github.com/kubernetes/kubernetes/issues/8144) (might have the underlying cause? I didn't look too far into it and just wanted to fix the issue. Maybe useful for further digging.) and [here](https://github.com/easzlab/kubeasz/issues/203). The second issue is in Chinese, but it mentioned Calico so I decided to dig a bit in that direction.

I used `kubectl logs` to look at the output of the `calico-node-*` pods. I noticed that during normal operation, it generates logs like these around every 5 seconds:

```
2020-06-18 12:16:25.352 [INFO][50] int_dataplane.go 907: Applying dataplane updates
2020-06-18 12:16:25.352 [INFO][50] table.go 740: Invalidating dataplane cache ipVersion=0x4 reason="refresh timer" table="mangle"
2020-06-18 12:16:25.354 [INFO][50] table.go 460: Loading current iptables state and checking it is correct. ipVersion=0x4 table="mangle"
2020-06-18 12:16:25.358 [INFO][50] int_dataplane.go 921: Finished applying updates to dataplane. msecToApply=5.601624999999999
```

However, on the broken chick11, the pod's logs were cut off on the 19th, around the time of the upgrade, and no new logs are generated after that. Using this I was able to query all chicks and find which ones have calico logs cut off early [[3]](#3), and it turns out chicks 11, 12, 15, 16, 17 and 18 are broken. One chick (I think it was chick15, but I can''t remember exactly and unfortunately I've lost the logs from the old container now) had its calico logs cut off since February, so maybe this issue goes back then as well, and we just got lucky since no pods were scheduled there, I'm not entirely sure.

## Solution

The GitHub issues didn't mention exactly how to fix it, so I tried cordon+drain+reboot+uncordon the nodes, but that didn't work. The issue seems to be Calico related (which would also maybe explain why DNS is not working, it's just networking in general being broken (I didn't test `ping 1.1.1.1`, I probably should've)), and it might have been because of an improper cleanup during an upgrade, so I cordon+drained the nodes, then did a `docker system prune` in hopes that it cleans up broken networking interfaces. After that, I rebooted and uncordoned the systems, and the problem seem to be fixed. I'm still not entirely sure what the issue was, or why chick13 and chick14 were also upgraded by me but wasn't affected by this issue. We should probably monitor those nodes closely for a couple of days just in case.


## Side notes

### 1

To investigate logs from an init container for a pod, I couldn't do `kubectl logs POD_NAME`, since the pod itself is still in its init stage. I had to do a `kubectl describe` to figure out what node it is scheduled on, get the container ID, then SSH into the chick manually and do a `sudo docker logs CONTAINER_ID`.

### 2
I know there are ways to set node affinities, but I didn't look up how to do that. I just tested by running `kubectl run test --image=debian:latest -- sleep 10000` to create a deployment that runs a debian pod, finding the name of the pod using `kubectl get pods`, and getting a shell in it using `kubectl exec -it POD_NAME bash`. Use `kubectl describe` to figure out which node it is scheduled on, `kubectl delete pod POD_NAME` to delete the pod and reschedule a new one on another node (and pray it gets scheduled onto a broken one so we can test stuff), and finally `kubectl delete deployment test` to clean up after ourselves.

### 3
I used this one-liner to query the last line of all `calico-node` logs. Maybe this might be useful to future debuggers.
```sh
for i in `kubectl get pods -n kube-system |grep calico-node|cut -f1 -d' '`; do echo -n "`kubectl get pod -n kube-system $i -o wide|grep -o 'chick[^ ]*'` $i "; kubectl logs -n kube-system $i --tail 1; done
```
