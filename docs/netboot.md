# netboot docs

basically a guide to how we set up bootp on the manager node

follwing a combo of mostly this:
https://wiki.debian.org/PXEBootInstall#Preface
and also
https://help.ubuntu.com/18.04/installation-guide/amd64/ch04s05.html
and a little bit of
https://linuxhint.com/pxe_boot_ubuntu_server/


For no good reason other than they used that in the tutorial above, I'm using
192.169.0.0/24 as the subnet and 192.168.0.1 as the manager node for the
management network.

### quick word on hardaware

  network booting seems to work only on the enp1s0 interface on nodes. This is
  currently the one on the left. You cannot boot on the management interface
  that is located on the far left of the machines. Furthermore, this didn't work
  initially on the smart switch, so you must make sure that there are not routes
  or something already configured that would cause unexpected behavior. You also
  need to make sure you are doing this on a private network where the manager is
  the only dhcp server.
  After they were initially booted, I was able to switch them all over to the
  smart switch and there were no problems.

### steps on rooster (i.e. commands to run on rooster to get netboot to work):

1. `sudo apt install isc-dhcp-server`

1. to `/etc/default/isc-dhcp-server` I added the line:

    INTERFACESv4="enp3s0"

  since enp3s0 is the interface that is hooked up to the management network.
  Here, we assume enp3s0 is the interface on the manager node that faces the
  internal kubernetes network.

1. to `/etc/netplan/01-netcfg.yaml`, or whatever the netplan file is I added
  the following under ethernets:
    
              enp3s0:
                  addresses: [192.168.0.1/24]
                  gateway4: 128.120.136.1
                  dhcp4: no
                  nameservers:
                          addresses: [192.168.0.1]
    
  so we get that management interface up

1. `netplan apply`

1. before changing `/etc/dhcp/dhcpd.conf` copy the current one to
  `/etc/dhcp/dhcpd.conf.backup` and set it to this
  ```conf
# the following is adapted from
# https://wiki.debian.org/PXEBootInstall#Preface
#
default-lease-time 600;
max-lease-time 7200;

allow booting;
allow bootp;

# in this example, we serve DHCP requests from 10.0.0.(3 to 253)
# and we have a router at 10.0.0.1
# these will be the name of the nodes.
subnet 10.0.0.0 netmask 255.255.255.0 {
  range 10.0.0.3 10.0.0.253;
  option broadcast-address 10.0.0.255;
  option routers 10.0.0.1;     # this ends up being the default gateway router
                               # on the hosts. Set to the manager so we can NAT
  option domain-name-servers 128.120.136.129,128.120.136.133,128.120.136.134;
  filename "pxelinux.0";
}

group {
  next-server 10.0.0.1;                # our Server. was previously 128.120.136.1
  host tftpclient {
    filename "pxelinux.0"; # (this we will provide later)
  }
}

  ```

1. `systemctl restart isc-dhcp-server` to get the dhcp server making
  repsjournalctl -fu isc-dhcp-server

1. checked the logs with `grep DHCP /var/log/syslog` and there were some
  requests and handouts, so thats good.

1. `sudo apt install tftpd-hpa`

1. changed `/etc/default/tftpd-hpa` to have these two defaults:
  ```
  TFTP_DIRECTORY="/srv/tftp"
  TFTP_OPTIONS="--secure -vvv"
  ```
  so we listen on our management net and not on the internet.
     ^- changed this, need to change it back after testing

1. `sudo mkdir /srv/tftp`

1. `systemctl restart tftpd-hpa` and then test it

1. `wget http://archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/current/images/netboot/netboot.tar.gz`

1. move netboot.tar.gz into `/srv/tftp` and run `tar xvzf netboot.tar.gz` and make the contents readable with `chmod -R a+r *`

1. `systemctl restart tftpd-hpa`

1. start up the client machine and it should get to a boot screen.

### configure NAT

1. `apt get ufw`

1. add the following to `/etc/ufw/before.rules`
```
*nat
:POSTROUTING ACCEPT [0:0]
# send stuff out of the eth2 iface
-A POSTROUTING -o enp2s0 -j MASQUERADE
COMMIT
```

  note that enp2s0 is the interface that faces the public internet

1. uncomment `net/ipv4/ip_forward=1` in `/etc/ufw/sysctl.conf`

1. `systemctl restart ufw`

1. `sudo ufw allow tftp` so it can use the images


# steps on chicks (i.e. things you need to do to boot a node on the network)

1. have it connected to enp1s0 which is the left ethernet port on the right side

1. power it on with the disks in. The install screen should come on. If not, you
  may have to change the boot priority order

1. go through the installation steps. Once it says "installing base system,"
  that part takes like an hour so you can go do something else. After that its
  mostly done.

1. after completing the installation, to get it to boot from disk, you have to
  turn off the network boot on the manager (rooster). So on rooster, run
  `systemctl stop tftpd-hpa` before rebooting your newly installed machine.
  After it boots, you can turn tftp back on.
