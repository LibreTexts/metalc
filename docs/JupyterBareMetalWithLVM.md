# Setting up a JupyterHub Bare-Metal Server on a Virtual Machine


# Setting up your VM with RAID 1 and LVM


## Source

[https://youtu.be/x2cNglQkSlc](https://youtu.be/x2cNglQkSlc)

I followed this video loosely. The amount of space I used and the number of disks are different.


## Creating the disks

Create 2 disks with 20 GB each.


## Partitioning disks

When reaching the partition disks stage:

Create a partition on each disk.

On each, choose:



*   Primary partition
*   Beginning location
*   Use as physical volume for RAID

The three partitions:



1. 1 primary partition, beginning location, with 2.0 GB. Use as physical volume for RAID, set the bootable flag on.
2. 1 primary partition, beginning location, with the leftover space (I had 19.5 GB). Use as physical volume for RAID.


## Configuring RAID 1

Choose Configure Software RAID1

We will create two MD devices.

To do so: Create MD Device, RAID 1, with 2 active devices and 0 spare devices.

Pair the following devices when creating:



*   /dev/sda1 and /dev/sdb1
*   /dev/sda2 and /dev/sdb2


## Create boot partition

In RAID1 device #0, select the 2.0 GB partition:

Use as Ext2 file system, set the mount point to /boot.


## Create logical volumes

Configure the Logical Volume Manager



*   Create volume group, name it VGsys. Select device as: /dev/md1.
*   Create logical volume, choose VGsys. Name it LVsys, give it 18 GB.
*   Create logical volume, choose VGsys. Name it LVswap, give it the default size (for me, it was 1455 MB).

Finish


### Choose the first partition:

LVM VG VGsys, LV LVswap

Use as swap area

Done setting up this partition


### Choose the second partition:

LVM VG VGsys, LV LVswap

#1 2.0 GB

Use as Ext4 journaling file system

Mount point: / - the root file system

Done setting up this partition

Finish partitioning and write changes to disk.


# Installing JupyterHub


## Source

Based on Kevin's instructions and the steps here: [https://github.com/mechmotum/jupyterhub-deploy-teaching](https://github.com/mechmotum/jupyterhub-deploy-teaching)


## Installing Ansible

Prerequisite step in Github instructions


```
$ sudo apt-get install ansible
```



## Clone the jupyterhub-deploy-teaching repository


```
$ git clone https://github.com/ixjlyons/jupyterhub-deploy-teaching.git
$ cd jupyterhub-deploy-teaching
$ git clone https://github.com/UDST/ansible-conda.git
```



## Change the hosts in the hosts file to your own username


```
$ cd group_vars
$ vim jupyterhub_hosts.example
```


Replace `<username>` with your own username.


```
jupyterhub_admin_users:
-  <username>

jupyterhub_users:
-  <username>
```


Rename juptyerhub_hosts.example to jupyter_hosts


```
$ mv jupyterhub_hosts.example jupyter_hosts
```



## Generate a proxy ID

Step 2 in Github instructions

Run openssl to generate proxy id


```
$ openssl rand -hex 32 > test.txt
```


Copy and paste test.txt into the jupyter_hosts file at the line: proxy_auth_token. If you're using vim, use 'y' to copy and 'p' to paste in the default mode (not insert mode).


## Generate a self-signed SSL certificate

SSL certificate:

Create self-signed ssl certificates to make nginx work

Source: [https://www.akadia.com/services/ssh_test_certificate.html](https://www.akadia.com/services/ssh_test_certificate.html)


```
$ cd security
$ openssl genrsa -des3 -out ssl.key 1024
$ openssl req -new -key ssl.key -out ssl.csr
$ cp ssl.key ssl.key.org
$ openssl rsa -in ssl.key.org -out ssl.key
$ openssl x509 -req -days 365 -in ssl.csr -signkey ssl.key -out ssl.crt
```



## Generate cookie secret

Step 5 in Github instructions

Navigate to the jupyterhub-deploy-teaching directory


```
$ cd ..
$ openssl rand -hex 32 > security/cookie_secret
```



## Update host IP and port in hosts file

Step 6 in Github instructions

Rename hosts.example to hosts


```
$ mv hosts.example hosts
```


In hosts, replace the last line of the file:


```
local ansible_ssh_host=127.0.0.1 ansible_ssh_port=22
```



## Generate an SSH key

In jupyterhub-deploy-teaching:


```
$ ssh-keygen
(hit enter for all)
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```



## Install python3-distutils

It is required.


```
$ sudo apt-get install python3-distutils
```



## Run ansible-playbook

Step 7 in Github instructions

Replace `<username>` with your own username.


```
$ ansible-playbook -l local-u <username> --ask-become-pass deploy.yml
```



## Running JupyterHub

Restart your VM


### Setting the hosts and guest ports to view the server locally

Go the VM settings →  Network

At this point adapter 1 should be attached to NAT. If not, change it

Go to advanced setting and click on port forwarding and add a rule and

Set Host Port to 8000 and Guest Port to 8000 also. Leave others blank.

Save the settings.

To SSH into your server from your local computer, run `ssh <username>@localhost -p 8000`.

### Run JupyterHub


```
$ jupyterhub
```

 **Note:** If jupyterhub is not running on a port, use:

```
$ sudo lsof -t -i:<port>
```

 to find id of process running on that port and kill it with:

```
$ sudo kill -9 <process id>
```

Go to `localhost:8000/`

Sign in with your username and password.
