# Networking

This will be where we put all the network info.

## public network

This is how all the computers will communicate with each other using kubernetes and how they will
access the internet.

blue ethernet cables. Plugged into the smart switch.

manager is at 128.120.136.26

enp1s0 on all the machines (the one on the left)

log into the switch with `screen /dev/ttyS0` on the management node
  - use username: manager
        password: friend

## Management Network

We will have one management node and one dumb switch for this network. The management node
will connect to it on its enp2s0(the ethernet port on the right) and its management
interface (the one all the way to the left next to the usb ports).
It will run a DHCP server on this network.
The rest of the nodes will connect to this dumb switch only on their management interface.

Use green ethernet cables.