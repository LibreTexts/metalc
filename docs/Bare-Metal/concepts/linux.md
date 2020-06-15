# Linux

This is a guide of the file system and common commands.

## Common commands
[This article](https://www.dummies.com/computers/operating-systems/linux/common-linux-commands/) 
covers a lot of Linux commands that are often used when navigating through
the file system.

## File system
* `/etc/` - where a lot of the configuration files for most programs are stored. If you `ls` in that directory,
you will find folders that are named after many programs
that are found in the computer.
* `/var/` - contains variable data, like logs.

## Debugging
* `systemctl` - commands help start, stop, or check the status of services.
  Some examples of systemctl commands on services include:
  * `sudo systemctl status <service-name>` - check the status of your specified service
  * `sudo systemctl start <service-name>` - start the service 
  * `sudo systemctl stop <service-name>` - stop the service
 > Example: `sudo systemctl status kubelet`

* `journalctl` - gives logs of a service
  * `journalctl -u <service-name> -r` - view logs of a service name starting from the most recent

## Networking
* `ip a` or `ip addr` shows the network interfaces. 
* `sudo ufw status` shows the current firewall restrictions and allowances

