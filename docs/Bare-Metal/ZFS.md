# Introduction
For the storage needs of our cluster, we have decided to setup a ZFS server. This decision was made partly because of the expertise and help that folks at the UC Davis Bioinformatics core could bring to the table, and because of the hardware already available to us. In addition, ZFS is one of the best filesystem for long-term, large-scale data storage, probably exceeding our needs for our current setup and for near future iterations of our cluster.

# Hardware
* ***Chassis:*** 4U rackmount server case 36 bay
* ***Motherboard:*** Supermicro X9DRH-7TF/7F/iTF/iF
* ***Memory:*** Samsung 16 GB DDR3
* ***HDD:*** Seagate Constellation ES.3 SAS 6Gb/s
* ***SSD:***
    * Intel SSD DC S3500 Series 120GB(will be referred to as 'Intel SSDs' in the rest of the document)
    * Seagate Enterprise SATA SSD 120GB(will be referred to as 'Seagate SSDs' in the rest of the document)

# Design

For data storage we used 4 stripes with raidz2, each stripe is compromised of 4 HDDs for storage and 2 HDDs for parity. The total number of HDDs that can fail per stripe without bringing the server down is 2. Our pool is made up of 24 total drives(16 storage + 8 parity). We opted to make our stripes only 6 HDDs wide so that we can have more stripes in total to improve read/write performance.

For the OS, we use Centos 7. The OS is running on 2 Seagate SSDs with RAID1 for redundancy. Separate partitions of 10GBs each are created with LVM for var and tmp, in order to prevent root from crashing in the case var and tmp take up all the space.

Since we expect more writes than reads, we have setup 2 Intel SSDs as the zil cache. Because of the known weakness of SSDs to writes, the Intel SSDs were over-provisioned to 70% of their capacity. This will improve their performance and increase their life expectancy greatly. Potentially in the future, we can also add some l2arc caches to improve read performance, but it seems that we won't need that for now.

On standby, we have two HDDs that act as hot spares to add an additional layer of security, If a HDD goes down in one of the stripes, one of the hot spares will be used to rebuild a stripe automatically without user intervention. In the event of a HDD failure, we plan to replace the failed drive with a new HDD and rebuild that stripe with that, so that we can keep the hot spares in the back of the chassis can just remain there.

In the near future, we plan to also add 2 SSDs as l2arc caches to improve the read performance from the cluster.

# Hardware Preparation
