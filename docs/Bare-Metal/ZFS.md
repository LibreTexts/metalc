# Table of Contents
1. [Introduction](#Introduction)
1. [Hardware](#Hardware)
1. [Design](#Design)
1. [Hardware Preparation](#Hardware-Preparation)
1. [Networking](#Networking)
1. [Installing CentOS 7](#Installing-CentOS-7)
1. [Setting up ZFS](#Setting-up-ZFS)
1. [Updating ZFS and Centos](#Updating-ZFS-and-Centos)
1. [Done](#Done)


# Introduction
For the storage needs of our cluster, we have decided to setup a ZFS server. This decision was made partly because of the expertise and help that folks at the UC Davis Bioinformatics core could bring to the table, and because of the hardware already available to us. In addition, ZFS is one of the best filesystem for long-term, large-scale data storage, probably exceeding our needs for our current setup and for near future iterations of our cluster.

# Hardware
* ***Chassis:*** 4U rackmount server case 36 bay
* ***Motherboard:*** Supermicro X9DRH-7TF/7F/iTF/iF
* ***Memory:*** Samsung 16 GB DDR3
* ***HDD:*** Seagate Constellation ES.3 SAS 6Gb/s(will be referred to as 'HDDs')
* ***SSD:***
    * Intel SSD DC S3500 Series 120GB(will be referred to as 'Intel SSDs' in the rest of the document)
    * Seagate Enterprise SATA SSD 120GB(will be referred to as 'Seagate SSDs' in the rest of the document)

# Design
For data storage we used 4 stripes with raidz2, each stripe is compromised of 4 HDDs for storage and 2 HDDs for parity. The total number of HDDs that can fail per stripe without bringing the server down is 2. Our pool is made up of 24 total drives(16 storage + 8 parity). We opted to make our stripes only 6 HDDs wide so that we can have more stripes in total to improve read/write performance.

For the OS, we use Centos 7. The OS is running on 2 Seagate SSDs with RAID1 for redundancy. Separate partitions of 10GBs each are created with LVM for var and tmp, in order to prevent root from crashing in the case var and tmp take up all the space.

Since we expect more writes than reads, we have setup 2 Intel SSDs as the zil cache. Because of the known weakness of SSDs to writes, the Intel SSDs were over-provisioned to 70% of their capacity. This will improve their performance and increase their life expectancy greatly. Potentially in the future, we can also add some l2arc caches to improve read performance, but it seems that we won't need that for now.

On standby, we have two HDDs that act as hot spares to add an additional layer of security. If a HDD goes down in one of the stripes, one of the hot spares will be used to rebuild a stripe automatically without user intervention. In the event of a HDD failure, we plan to replace the failed drive with a new HDD and rebuild that stripe with that, so that the hot spares in the back of the chassis can just remain there.

# Hardware Preparation
It is critical to update all the hardware when setting up a new server, since it will be very hard to do so once it runs in production. In this section, some of the details regarding the specific hardware that we had will be covered along with some tips.

All of the hardware that we used to setup our ZFS server was made available to us by the UC Davis Bioinformatics Core, and luckily it well exceeds our needs.

## Chassis
The chassis that we have is a standard 4U rackmount server case with 36 bays. 24 bays are in the front, and 12 are in the back. The data and parity HDDs will be in the front bay for easy access, and the 2 zil caches, 2 OS Seagate SSDs and the 2 hot spares will be in the back.

## Motherboard
The Supermicro X9DRH-7TF/7F/iTF/iF motherboard needed to be updated. The BIOS was at version 3.0a when it was first booted, with 3.3 being the newest version. Also the IPMI controller firmware was updated.

For Supermicro X9DRH-7TF/7F/iTF/iF, in order to update and flash the BIOS, two jumpers needed to be placed on the motherboard. This is a safety feature to prevent unauthorized people from trying to tamper with the BIOS.

A DOS was used to update both the BIOS and the IPMI, the BIOS and IPMI can be found at [Supermicro](https://www.supermicro.com/products/motherboard/xeon/c600/x9drh-7tf.cfm)'s website.

## Memory
We used 16 sticks of 16GBs DDR3 RAM, totaling up to 256 GBs of total RAM.

## HDD
The Seagate Constellation ES.3 SAS 6Gb/s drives also needed to be updated to the latest firmware. One can check the latest firmware available at the [Seagate website](https://www.seagate.com/support/internal-hard-drives/enterprise-hard-drives/constellation-es/), at the bottom left corner of the page, there is a search function for the serial number on the drive.

Seagate does a good job at providing users with a variety of tools for updating their firmware, and an easy to understand guide on how to doing so. All the tools, firmware updates and the guide are neatly packaged in the single folder that you download on the website.

We used the linux cli tool to update the firmware, and it was very straightforward. We inserted all the drives in the bays and run a single command to update all the firmwares sequentially.

## SSD
### Intel SSD DC S3500 Series 120GB
Intel provides a couple of very good tools for firmware updates and just general benchmarking. The tool that we used was the [Intel Solid State Drive Toolbox](https://downloadcenter.intel.com/download/28808/Intel-Solid-State-Drive-Toolbox), which is only available for Windows, but it allows you to update the firmware of your Intel SSD in the click of one button, and it can check the health state of your SSD.

To increase the performance and life expectancy of an SSD, it is suggested to overprovision them. Overprovisioning is the act of "reducing" the maximum amount of storage available to the user, so there is always some free storage on the SSD. By always having free storage available, the endurance of the SSD is improved as the total number of writes and erases can be distributed across a larger population of NAND flash blocks.

Intel has a [white paper](https://www.intel.com/content/dam/www/public/us/en/documents/white-papers/over-provisioning-nand-based-ssds-better-endurance-whitepaper.pdf) on overprovisioning. We followed the using 'Using Intel SSD Data Center Tool for Over-Provisioning' section. We set the capacity to ```MaximumLBA=70%```, we overprovisioned a little more than the suggested amount of 80% because we planned to use these as the zil caches for the ZFS, so we knew that there would be a lot of writing and erasing going to happen on the drive.

### Seagate Enterprise SATA SSD 120GB
The Seagate SSDs can be updated using similar tools used for updating the Seagate HDDs. To find the right tools and instructions to update the drive, the [Seagate website](https://www.seagate.com/support/internal-hard-drives/enterprise-hard-drives/constellation-es/) provides a way to check for firmware updates, at the bottom left corner of the page one can use the serial number of the drive to do a quick look up.

The process was similar to updating the HDDs, and we used the linux cli tool again.

We also overprovision the Seagate SSDs by leaving some free space when we install CentOS.

# Networking
***Note:*** If you are using an intel network interface card you might run into compatibilities problem with the driver. Follow [these](https://ahelpme.com/linux/kernel/missing-network-interface-10g-intel-x520-with-error-failed-to-load-because-of-unsupported-sfp/) instructions to solve the problem.

It is best to have the ZFS on a faster connection compared to the nodes that it will interact with. In our case, our ZFS server has a 10Gbps network card, and the rest of the nodes run on a 1Gbps.

The ZFS server is connected to our smart switch using a short distance SFP+ transceiver with a 10 meters SR(multimode) copper wire cable. The worker nodes then are connected to the smart switch using a standard ethernet cable.

***Note:*** The transceiver and cable type have to match in order to work. For example, if the transceivers being used are multimode then the cable has to be multimode. Same goes for single mode. More info can be found [here](https://community.fs.com/blog/how-many-types-of-sfp-transceivers-do-you-know.html).

We have a DHCP server running on rooster, and this is how our ZFS server gets assigned an ip on the k8s network.


# Installing CentOS 7
For our CentOS installation, we burned the [minimal ISO](https://www.centos.org/download/) of CentOS onto a USB and used it as a bootable device.

After booting into the drive, you should be greeted by seeing the CentOS installation screen. Here one can customize options such as keyboard language, OS language network, and various other options. Clicking on the 'Installation Destination' option, here we pick the drives to where the OS will be installed. For our setup, we will use a simple RAID1 setup with our 2 overprovisioned Seagate SSDs for redundancy and performance. After choosing the destination of the installation, we check the option 'I will configure partitioning' and click 'Done'.

At this point, we will be presented with the manual partitioning screen. We delete any partition currently present on the drives that we have chosen and proceed to create our own. We choose the 'LVM' partitioning scheme and start by creating the /boot partition. We assign a size of 4GB to it, and set the filesystem type to ext4 and the 'RAID level' to RAID1. Next, we create the /swap partition, and also assign a size of 4GB to it, and leave the filesystem type to 'swap' and set the 'RAID level' to RAID1. We also make partitions for /var and /tmp, each one with 10GB of storage and ext4 and RAID1. Finally, we create the root partition (/) with a size of 60GB and ext4 and RAID1.

***Note:*** It is important to create seperate partitions for /tmp and /var, as these folders tend to take up a lot of space, so that we don't run the risk of crashing the OS in the event they fill up too much.

After we are done with the manual partitioning of the installation, CentOS will start installing. When CentOS is installing, it is a good time to setup the root password and create an account if one desires.

***Important:*** By default, CentOS disables the network interface cards, and they have to be enabled before any kind of networking works. To enabled the cards, we run this command first ```cd /etc/sysconfig/network-scripts/```, here we will find some files with the name of the nic(network interface cards) available. Something like this:
```
ifcfg-enp3s0f0      ifcfg-enp6s0f1  ifdown-eth   ifdown-isdn    ifdown-sit       ifup          ifup-ib    ifup-plip   ifup-routes    ifup-tunnel        network-functions-ipv6
ifcfg-enp3s0f0.bak  ifcfg-lo        ifdown-ib    ifdown-post    ifdown-Team      ifup-aliases  ifup-ippp  ifup-plusb  ifup-sit       ifup-wireless
ifcfg-enp3s0f1      ifdown          ifdown-ippp  ifdown-ppp     ifdown-TeamPort  ifup-bnep     ifup-ipv6  ifup-post   ifup-Team      init.ipv6-global
ifcfg-enp6s0f0      ifdown-bnep     ifdown-ipv6  ifdown-routes  ifdown-tunnel    ifup-eth      ifup-isdn  ifup-ppp    ifup-TeamPort  network-functions
```
We go into each one of the 'ifcfg-enp*' files and edit them by changing the 'ONBOOT' option from 'no' to 'yes':
```diff
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=dhcp
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=enp3s0f0
UUID=<your UUID>
DEVICE=enp3s0f0
-ONBOOT=no
+ONBOOT=yes
ZONE=public
```
We reboot the system, and now the networking should work.

This is also a good time to install package updates, so we run ```sudo yum check-update``` followed by ```sudo yum update```.

# Setting up ZFS
## Installing ZFS
***Note:*** As of 9/4/19, version 0.8.1-1, which is development version at this moment, is less buggy than version 0.7.*, so that's the version we used.

The ZFS repository provides some good documentation on how to install ZFS for a variety of OSes, the one that we will be looking at will be the [RHEL and CentOS](https://github.com/zfsonlinux/zfs/wiki/RHEL-and-CentOS) one.

Following the guide, we install the latest EL package(EL7.6 at the moment):
```
sudo yum install http://download.zfsonlinux.org/epel/zfs-release.el7_6.noarch.rpm
```
We then run these commands to complete the installation of ZFS:
```
sudo yum install epel-release
sudo yum --enablerepo=zfs-testing install kernel-devel zfs
```
***Note:*** If after running ```zfs --version``` you don't get anything, try running ```modprobe zfs```.

## Creating a zpool
For our setup, we use the front 24 bays(6 rows x 4 columns) for our stripes/vdevs, and in the remaining 12 bays in the back of the rack we have our 2 zil caches, 2 OS drives and 2 hot spares.

It is highly suggested to insert one stripe at a time and record the ids of the drives. This will be extremely helpful for future maintenance and locating failed drives.

We used ledctl to find the ids of the drives, it can be easily installed with ```sudo yum install ledctl```. After inserting the first stripe, we navigate to /dev/ and run ```sudo ledctl <sd* address>``` and check if there is a led blinking in our stripe. Once we locate a drive on the stripe, we go to ```cd /dev/disk/by-id``` and run ```ls -l``` and it will show us what sd* has what id.
```
lrwxrwxrwx. 1 root root  9 Aug 28 18:19 scsi-35000c50057f4bedb -> ../../sdy
lrwxrwxrwx. 1 root root 10 Aug 28 18:19 scsi-35000c50057f4bedb-part1 -> ../../sdy1
lrwxrwxrwx. 1 root root 10 Aug 28 18:19 scsi-35000c50057f4bedb-part9 -> ../../sdy9
lrwxrwxrwx. 1 root root  9 Aug 28 18:19 scsi-35000c50057f5d163 -> ../../sdn
lrwxrwxrwx. 1 root root 10 Aug 28 18:19 scsi-35000c50057f5d163-part1 -> ../../sdn1
lrwxrwxrwx. 1 root root 10 Aug 28 18:19 scsi-35000c50057f5d163-part9 -> ../../sdn9
lrwxrwxrwx. 1 root root  9 Aug 28 18:19 scsi-35000c50057f625e3 -> ../../sdu
lrwxrwxrwx. 1 root root 10 Aug 28 18:19 scsi-35000c50057f625e3-part1 -> ../../sdu1
lrwxrwxrwx. 1 root root 10 Aug 28 18:19 scsi-35000c50057f625e3-part9 -> ../../sdu9
lrwxrwxrwx. 1 root root  9 Aug 28 18:19 scsi-35000c50058161edb -> ../../sdi

```
We record down the ids in a text file and find the ids for the rest of the drives in the same way. We should end up with a final text file like this:
```
Stripe 1:
  scsi-35000c500585b835b
  scsi-35000c500585b7687
  scsi-35000c500585b5c3b
  scsi-35000c500585bba67
  scsi-35000c500585babd3
  scsi-35000c500585b977b

Stripe 2:
  scsi-35000c500585b7ef3
  scsi-35000c500585b7713
  scsi-35000c500585b640f
  scsi-35000c500585b8f5f
  scsi-35000c50057f625e3
  scsi-35000c50058161edb

Stripe 3:
  scsi-35000c500585bb363
  scsi-35000c500585b7723
  scsi-35000c50057f5d163
  scsi-35000c50057f4bedb
  scsi-35000c5005816249f
  scsi-35000c500585baf5b

Stripe 4:
  scsi-35000c500585ba3a7
  scsi-35000c500585be40f
  scsi-35000c500585bbbbb
  scsi-35000c500585bcd97
  scsi-35000c500585bc6a7
  scsi-35000c500585b5c0b

Hot Spares:
  scsi-35000c500585b70cb
  scsi-35000c500585bb737

ZIL Cache:
  ata-INTEL_SSDSC2BB120G4_BTWL3441025V120LGN
  ata-INTEL_SSDSC2BB120G4_BTWL344200K7120LGN

```
***Important:*** For production zpool deployments, it is necessary to use drive ids when creating a pool instead of the sd* identifiers.

Once we have found all the ids for the drives, we create the zpool by running the command:
```
zpool create -o ashift=12 -f <name of the pool> raidz2 <stripe1 ids> raidz2 <stripe2 ids> raidz2 <stripe3 ids> raidz2 <stripe4 ids>
```
***ashift:*** This argument sets the minimum size of a IO on a vdev, 12 is for 4k drives. Matching the IO size with the drives you have will increase the performance of your ZFS.  
***raidz2:*** raidz2 creates a vdev that uses 2 disks for parity allowing up to 2 disks to fail in a vdev and the vdev would still work.

Then we can add the zil cache drives:
```
zpool add <name of the pool> log mirror <ssd ids>
```
***Note:*** Use SSDs for zil cache.

To add some hot spares to the pool:
```
zpool add <name of the pool> spare <spare drive id>
```

Optional step is to add compression to the zpool to increse the capacity, this works best when the data being stored is not compressed already. There are different types of compression available, the most common one is lze:
```
zpool set compression=lz4 <pool>
```

## Integrating ZFS with Kubernetes
### On the ZFS server
This part will assume that the ZFS is running CentOS 7.

SSH onto the ZFS server and setup a nfs server:
```
yum install -y nfs-utils
```
Once installed, enable the services:
```
systemctl start nfs-server rpcbind
systemctl enable nfs-server rpcbind
```
Set the permissions to allow NFS clients to read and write to the created directory:
```
chmod 777 /<name of your share>/
```
We have to modify /etc/exports to make an entry for the ZFS that we want to share:
```
/<name of your share> <ip address of the ZFS server with subnet mask>(rw,fsid=0,async,no_subtree_check,no_auth_nlm,insecure,no_root_squash)
```
Export the shared directory ussing the following command:
```
exportfs -r
```
Next we configure the firewall to allow other nodes to access the share on the ZFS server:
```
firewall-cmd --permanent --add-service mountd
firewall-cmd --permanent --add-service rpc-bind
firewall-cmd --permanent --add-service nfs
firewall-cmd --reload
```

### On the nodes using the ZFS
The last step is to login into the nodes and mount the ZFS share on there. It can be done through Ansible or manually. We create a local folder for the share and run:
```
mount <ip of the ZFS server>:/<name of the share on the ZFS server> /<local share folder name>
```

### Setting up nfs-client-provisioner
Create a config.yaml file with:
```
# values as specified in this:
# https://github.com/helm/charts/tree/master/stable/nfs-client-provisioner
#
# # set the nfs server to the host you are running on
nfs:
  server: <ip of the ZFS server>
# note that path can be '/' because we use the "fsid=0" param in `/etc/exports`
  path: /

# create a storage class with this provisioner and make it the default class
# reclaim policy Retain means people can sign back in and still have their
# stuff there
storageClass:
  defaultClass: true
  reclaimPolicy: Retain
```
Install the chart with our configurations:
```
helm install --name nfs-client-release stable/nfs-client-provisioner -f config.yml
```

### Tuning nfs-server
The nfs-server comes with a default of 8 threads, which if fairly low, it recommended to increase the threads number to accommodate for heavier loads. We have raise our number of threads to 512.

To change the number of threads, we change the configuration file at /etc/sysconfig/nfs:
```
sudo vim /etc/sysconfig/nfs
```
We change the `RPCNFSDCOUNT` parameter to the number of threads we want:
```diff
# Note: For new values to take effect the nfs-config service
# has to be restarted with the following command:
#    systemctl restart nfs-config
#
# Optional arguments passed to in-kernel lockd
#LOCKDARG=
# TCP port rpc.lockd should listen on.
#LOCKD_TCPPORT=32803
# UDP port rpc.lockd should listen on.
#LOCKD_UDPPORT=32769
#
# Optional arguments passed to rpc.nfsd. See rpc.nfsd(8)
RPCNFSDARGS=""
# Number of nfs server processes to be started.
# The default is 8.
-RPCNFSDCOUNT=
+RPCNFSDCOUNT=512
#
# Set V4 grace period in seconds
#NFSD_V4_GRACE=90
#
# Set V4 lease period in seconds
#NFSD_V4_LEASE=90
#
```
Then we restart the nfs-server with:
```
sudo service nfs-server restart
```
To check that the thread numbers have changed, we run `cat /proc/net/rpc/nfsd` and look at the row that says `th`. The first
column in that row is the number of threads running:
```
rc 0 80 1724228437
fh 13 0 0 0 0
io 1276009525 4004549293
th 511 0 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000
ra 32 0 0 0 0 0 0 0 0 0 0 0
net 1724182210 0 1724199642 1716321847
rpc 1724233643 0 0 0 0
proc3 22 110 957 22 54 41 0 0 17 21 8 0 0 12 0 0 0 0 36 249 118 59 0
proc4 2 187 1724229556
proc4ops 72 0 0 0 283322 277380 92 2950 0 7998 2976415 159260 147 1471402 0 1115825 178521 0 0 280797 0 0 41 7332238 0 948 1472379 4742 0 123236 789 0 146 936 0 36300 0 0 0 531747 0 0 1 384 213 186 498725 0 0 0 0 0 0 472 7929603 0 0 0 198 193 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Updating ZFS and Centos
If you need to just update the ZFS version, then a simple command like `yum upgrade zfs`. I would check with someone more knowledgeable first before you do this(Richard/Mike/Dean). In this section, I will discuss how to update a ZFS server that is in production, and what are the best practices to update both the Centos OS and the ZFS version running on it.

#### Pre-Update Tasks
1. Make sure to schedule a time for the services running on the cluster to be down way in adavance. Inform the users of the downtime, and keep them updated with any updates on the status of the cluster.
1. It is ***strongly*** to use a pair of new SSDs for the OS instead of just updating the OS on the production pair of SSDs.
1. Take this opportunity to update any major firmware/driver releases.
1. Download the Centos OS iso and burn it to a usb stick for easy installation.

#### Updating the OS
Shut the ZFS down, and replace the OS drives in the back of the ZFS. Once the new drives are in, use the usb to install the new version of Centos. Follow instructions in the ["Installing CentOS 7"](#Installing-CentOS-7) section to complete the installation.

#### Install the ZFS
If installing the released version of ZFS, and not the development version, the instructions [here](https://github.com/zfsonlinux/zfs/wiki/RHEL-and-CentOS) are easy and straightforward.

#### Rebuilding ZFS from Existing Drives
To import a zpool present in the drives after a new install, we use `sudo zpool import <name of zpool>`.

#### Reintegrating ZFS with Kubernetes
Follow the steps under [Integrating ZFS with Kubernetes](#Integrating-ZFS-with-Kubernetes).

# Done
Enjoy your ZFS !
