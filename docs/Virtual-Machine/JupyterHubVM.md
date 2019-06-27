# Setting up JupyterHub on a Virtual Machine


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

Follow the instructions outlined under the [Provisioning section](https://github.com/LibreTexts/jupyterhub-deploy-teaching/blob/bicycle/README.rst#Provisioning) 
of the LibreTexts fork of jupyterhub-deploy-teaching repository.

## Running JupyterHub

Restart your VM.


### Setting the hosts and guest ports to view the server locally

Go the VM settings →  Network

At this point adapter 1 should be attached to NAT. If not, change it

Go to advanced setting and click on port forwarding and add a rule and

Set Host Port to 8000 and Guest Port to 8000 also. Leave others blank.

Save the settings.

To SSH into your server from your local computer, run `ssh <username>@localhost -p 8000`.

### Run JupyterHub

Run the command:
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
