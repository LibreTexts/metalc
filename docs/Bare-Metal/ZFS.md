# Table of Contents
1. [Introduction](#Introduction)
1. [Hardware](#Hardware)
1. [Design](#Design)
1. [Hardware Preparation](#Hardware-Preparation)
1. [Installing CentOS 7](#Installing-CentOS-7)
1. [Setting up ZFS](#Setting-up-ZFS)


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

# Installing CentOS 7
For our CentOS installation, we burned the [minimal ISO](https://www.centos.org/download/) of CentOS onto a USB and used it as a bootable device.

After booting into the drive, you should be greeted by seeing the CentOS installation screen. Here one can customize options such as keyboard language, OS language network, and various other options. Clicking on the 'Installation Destination' option, here we pick the drives to where the OS will be installed. For our setup, we will use a simple RAID1 setup with our 2 overprovisioned Seagate SSDs for redundancy and performance. After choosing the destination of the installation, we check the option 'I will configure partitioning' and click 'Done'.

At this point, we will be presented with the manual partitioning screen. We delete any partition currently present on the drives that we have chosen and proceed to create our own. We choose the 'LVM' partitioning scheme and start by creating the /boot partition. We assign a size of 4GB to it, and set the filesystem type to ext4 and the 'RAID level' to RAID1. Next, we create the /swap partition, and also assign a size of 4GB to it, and leave the filesystem type to 'swap' and set the 'RAID level' to RAID1. We also make partitions for /var and /tmp, each one with 10GB of storage and ext4 and RAID1. Finally, we create the root partition (/) with a size of 60GB and ext4 and RAID1.

***Note:*** It is important to create seperate partitions for /tmp and /var, as these folders tend to take up a lot of space, so that we don't run the risk of crashing the OS in the event they fill up too much.

After we are done with the manual partitioning of the installation, CentOS will start installing. When CentOS is installing, it is a good time to setup the root password and create an account if one desires.

***Note:*** By default, CentOS disables the network interface cards, and they have to be enabled before any kind of networking works. To enabled the cards, we run this command first ```cd /etc/sysconfig/network-scripts/```, here we will find some files with the name of the nic(network interface cards) available. Something like this:
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
