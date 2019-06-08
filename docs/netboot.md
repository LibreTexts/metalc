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

### steps on rooster:

  1. `sudo apt install isc-dhcp-server`

  2. to `/etc/default/isc-dhcp-server` I added the line:
    
    INTERFACESv4="enp3s0"
    
  since enp3s0 is the interface that is hooked up to the management network.
  Here, we assume enp3s0 is the interface on the manager node that faces the
  internal kubernetes network.

  3. to `/etc/netplan/01-netcfg.yaml` or whatever the netplan file is I added
    the following under ethernets
    
              enp3s0:
                  addresses: [192.168.0.1/24]
                  gateway4: 128.120.136.1
                  dhcp4: no
                  nameservers:
                          addresses: [192.168.0.1]
    
  so we get that management interface up

  4. `netplan apply`

  5. `systemctl restart isc-dhcp-server` to get the dhcp server making
    repsjournalctl -fu isc-dhcp-server

  6. checked the logs with `grep DHCP /var/log/syslog` and there were some
    requests and handouts, so thats good.

  7. `sudo apt install tftpd-hpa`

  8. changed `/etc/default/tftpd-hpa` to have these two defaults:
    ```
    TFTP_DIRECTORY="/srv/tftp"
    TFTP_OPTIONS="--secure -vvv"
    ```
    so we listen on our management net and not on the internet.
       ^- changed this, need to change it back after testing

  9. `sudo mkdir /srv/tftp`

  10. `systemctl restart tftpd-hpa` and then test it

  11. `wget http://archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/current/images/netboot/netboot.tar.gz`

  12. move netboot.tar.gz into `/srv/tftp` and run `tar xvzf netboot.tar.gz` and make the contents readable with `chmod -R a+r *`

  13. `systemctl restart tftpd-hpa`

  14. start up the client machine and it should get to a boot screen.

### configure NAT

  15. `apt get ufw`

  16. add the following to `/etc/ufw/before.rules`
    ```
    *nat
    :POSTROUTING ACCEPT [0:0]
    # send stuff out of the eth2 iface
    -A POSTROUTING -o enp2s0 -j MASQUERADE
    COMMIT
    ```
    note that enp2s0 is the interface that faces the public internet

  17. uncomment `net/ipv4/ip_forward=1` in `/etc/ufw/sysctl.conf`

  18. `systemctl restart ufw`

  19. `sudo ufw allow tftp` so it can use the images
