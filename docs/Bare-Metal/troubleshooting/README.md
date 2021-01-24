# Common Practices For Troubleshooting 

If the troubleshooting that you are doing for a particular problem is ineffective it can largely be due to any of the following reasons:

1. You may be looking at symptoms unrelated to the problem.
   * Fixing this is a matter of becoming better aquainted with the system. The following are some resources that you may want to review:
      1. Documentation in galaxy-control-repo
      2. [BinderHub](/docs/Binder-on-GCloud/01-BinderHub.md)
      3. [Maintenance](/docs/maintenance-tasks.md)
      4. [Adding new packages to the Dockerfile](https://github.com/LibreTexts/default-env/)
2. Not fully understanding how to change the system such the inputs, outputs, the environment, and etc.
   * This is similar to the previous example, make sure you have good knowledge of the system you are looking at. Visit any of the above links, and feel free
   check out any other documentation. The following may potentially be relevant:
      1. [Introduction to Kubernetes](https://www.digitalocean.com/community/tutorials/an-introduction-to-kubernetes)
      2. [What is Docker?](https://opensource.com/resources/what-docker)
      3. [BinderHub FAQ](https://mybinder.readthedocs.io/en/latest/faq.html) 
3. Assuming that the problem you are facing is the same as one you have previously dealt with given that the symptoms are the same. 
   * If you are dealing with similar symptoms definitly look into how you have previously handled the issue, or how solutions have been documented
   [here](/docs/Bare-Metal/troubleshooting/). Howevever, if you have tried everything you 
   have done before, it might be worth trying something different. A good example of this kind of dilema is [this issue](https://github.com/LibreTexts/metalc/blob/master/docs/Bare-Metal/troubleshooting/KubeadmCert.md)
   we had.
      
      
## Checking the Logs: Journalctl

The journal is implemented through the `journald` daemon, a UNIX or LINUX program that runs in the background. It handles the messages
produced by the kernal. If you want to see what the logs have been picking up, you can run the `journalctl` command. Keep in mind that the 
oldest entries will be at the top. 

The command can be run by itself. 
```
$ journalctl
```
```
-- Logs begin at Wed 2020-04-22 12:43:49 PDT, end at Sun 2020-06-14 22:26:32 PDT
Apr 22 12:43:49 rooster sshd[22610]: Timeout, client not responding.
Apr 24 00:33:46 rooster kernel: [IPTABLES] IN=enp2s0 OUT= MAC=01:00:5e:00:00:01:
Apr 24 00:33:47 rooster kernel: [IPTABLES] IN=enp2s0 OUT= MAC=01:00:5e:00:00:01:
Apr 24 00:33:47 rooster kernel: [IPTABLES] IN=enp2s0 OUT= MAC=01:00:5e:00:00:01:
Apr 24 00:33:47 rooster kernel: [IPTABLES] IN=enp2s0 OUT= MAC=01:00:5e:00:00:01:
Apr 24 00:33:53 rooster kernel: [UFW BLOCK] IN=enp2s0 OUT= MAC=01:00:5e:00:00:01
Apr 24 00:33:53 rooster kernel: [IPTABLES] IN=enp2s0 OUT= MAC=01:00:5e:00:00:01:
Apr 24 00:33:53 rooster kernel: [IPTABLES] IN=enp2s0 OUT= MAC=01:00:5e:00:00:01:
Apr 24 00:33:53 rooster kernel: [IPTABLES] IN=enp2s0 OUT= MAC=01:00:5e:00:00:01:
Apr 24 00:33:53 rooster kernel: [IPTABLES] IN=enp2s0 OUT= MAC=01:00:5e:00:00:01:
Apr 24 00:33:54 rooster dhcpd[1459]: uid lease 10.0.0.12 for client 00:25:90:53:
....
....
....
....
Jun 14 00:00:00 rooster dhcpd[1459]: uid lease 10.0.0.4 for client 00:25:90:53:41
Jun 14 00:00:00 rooster dhcpd[1459]: DHCPREQUEST for 10.0.0.102 from 00:25:90:53:
```

Or amendments can be made. You may be interested in seeing information from a specific time, in which case your formatting will need to 
be absolute `YYYY-MM-DD HH:MM:SS`.

For example if you want records from May 4, 2019 at 6:13 PM:
```
$ journalctl --since "2019-05-04 18:13:00"
```
Keep in mind if you omit certain parts, journalctl will make assumptions. If you leave out the date, it will assume the current date, and 
if the time is left out, then it will assume the time to be ``00:00:00`` or 12 am at 0 minutes and 0 seconds. 

You can also filter out the logs depending on the service. 
```
$ journalctl -u <service name>.service
```

You can also add the `-r` option to sort logs by most recent first.
```
$ journalctl -u <service-name> -r
```

## Is this Thing Even On?: Systemctl

``systemctl`` is a good tool to use to start, stop, restart, check status, and etc. for different services. It is part of ``sytstemd``. ``systemd``
initializes the *user space* components that run after the kernal is booted. The following are some commands that you can use, simply
replace ``<service name>`` with the one you are using:

Keep in mind that it is not necassary to include `.service `.

`$ sudo systemctl start <service name>.service`: starts a `systemd` service

`$ sudo systemctl stop <service name>.service`: stops a `systemd` service

Note for the enable/disable options, the commands do not start the service in the current session. You will need to add `--now` to do so.

`$ sudo systemctl enable <service name>`: enables the service at boot

`$ sudo systemctl disable <service name>`: disables the service at boot

`$ systemctl status <service name>`: checks the status of the service

## Basic Tips for Kubernetes

Here are a few helpful tips to deubgging application deployed into Kubernetes:

**Debugging Pods**

`$ kubectl describe pods ${POD_NAME}`: Tells you the current state of the Pod and recent events 
  * if you see `Pending`, that means your Pod cannot be scheduled onto a node, a common reason for this is that you do not have 
    enough resources. Look back at the output for `kubectl describe...` and it should give you a reason
  * if you see `Waiting`, that means your Pod has been scheduled to a worker node, but it can't run on that machine. Make sure your image
    name is correct. Run `docker pull <image>` to if you can pull your image.

**Debugging Services**

`$ kubectl get endpoints ${SERVICE_NAME}`: verify that there are endpoints for the service, and make sure that the endpoints match up with 
the number of containers that you expect to be a member of your service.
 > For example, if your Service is for an nginx container with 3 replicas, you would expect to see three different IP addresses 
 in the Service's endpoints.


## Resources
- [Effective Troubleshooting](https://landing.google.com/sre/sre-book/chapters/effective-troubleshooting/)
- [How To Use Journalctl to View and Manipulate Systemd Logs](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs)
- [Use journalctl to View Your System's Logs](https://www.linode.com/docs/quick-answers/linux/how-to-use-journalctl/)
- [Introduction to systemctl](https://www.linode.com/docs/quick-answers/linux-essentials/introduction-to-systemctl/)
- [How To Use Systemctl to Manage Systemd Services and Units](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)
- [Kubernetes Troubleshooting](https://kubernetes.io/docs/tasks/debug-application-cluster/troubleshooting/)
- [More Troubleshooting with Kubernetes](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-application/)


