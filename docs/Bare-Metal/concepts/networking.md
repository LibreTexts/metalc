# Networking
*Relevant files: `/etc/netplan/`* *Summary: https://netplan.io/examples*

We use [netplan](https://netplan.io/) to configure networking on rooster.

In `/etc/netplan/01-netcfg.yaml`, you can see different network interfaces.
As you can see, there are different networks defined (the public
Internet network, the private Kubernetes network where chicks are
assigned specific IP addresses, and a management network).

[This Microsoft
article](https://support.microsoft.com/en-us/help/164015/understanding-tcp-ip-addressing-and-subnetting-basics)
and [Wikipedia
article](https://en.wikipedia.org/wiki/Subnetwork#Network_addressing_and_routing)
explains IP addresses and subnet masks. They are a bit detailed,
but you only need to get the general idea.

> An IP address is a 32-bit number that uniquely identifies a host
> (computer or other device, such as a printer or router) on a TCP/IP
> network.

> The second item, which is required for TCP/IP to work, is the subnet
> mask. The subnet mask is used by the TCP/IP protocol to determine whether
> a host is on the local subnet or on a remote network.

A network interface in Linux is a software that lets you access and
configure network hardware. 

You can find your IP address and network interfaces by running the command
`ip a` or `ifconfig`. [This article does a great job explaining the
output](https://goinbigdata.com/demystifying-ifconfig-and-network-interfaces-in-linux/) of these commands!

If you run `ip a` on rooster, you will be able to see the networks defined
in netplan.
