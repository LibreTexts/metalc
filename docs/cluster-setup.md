# Cluster Setup

Where we document how we get the cluster setup and working.

## Pod Network

pod CIDR is 10.244.0.0/16

Choosing calico. The manifest is in the home directory of the repo `calico.yaml`.
In this we changed:

    CALICO_IPV4_IPIP: "Never"
    CALICO_IPV4POOL_CIDER: "10.244.0.0/16"

## Rooster (management node)

Not going to be part of the kubernetes cluster. It
runs a dhcp server and acts as a gateway to the internet and does NAT.

Might use it to do some load balancing for the luster and assign IP's with
metalc, but we'll see about that later.

## Chicks (standard nodes)

We are calling the basic nodes chicks. These will be our masters and workers in
the kubernetes cluster.

Each has hostname `chick{i}` where i is a natural number.

Currently have `chick0` through `chick10` so 11 in total.

Assinging static IPs for `chick{i}` of `10.0.0.{i + 100}`. So `chick0` will be
at `10.0.0.100` and `chick1` at `10.0.0.101`, etc.


## Adding Nodes

First, check out `netboot.md`. This will cover what you have to do to get the
node functioning in the kubernetes cluster after the os is already installed.

1. figure out the ip address that was assigned by the manager's dhcp server by
  checking out the logs on rooster. Logs are in `/var/log/syslog` for dhcp, so
  run something like `grep dhcp /var/log/syslog` and there will be mention of
  what ip it was assigned.

1. Add the node to `chicks.csv` by manually adding the hostname and the ip address
  and other fields. Then, on rooster run `./get_macs.py`
  and this will automatically fill in the `enp1s0` and `enp2s0` fields with the
  mac address on those interfaces. See the comments at `get_macs.py`.

1. Optionally assign a static ip address to the host by changing
  `/etc/dhcp/dhcpd.conf` on the master and adding the mac address and the ip
  address you want. See the comments and other examples in that file.
  Then run `systemctl restart isc-dhcp-server`. It will
  take a little while for the node's current ip lease to expire and for it to
  recieve the new IP. Sadly, we [cant speed this up](
  https://stackoverflow.com/questions/28917135/how-to-force-all-of-the-dhcp-clients-to-renew)
