# RAID

.Redundant Array of Independent Disks.

**Why?**



1. For **speed of operation**, you want to minimize the access time.
1. For **data redundancy**, if any one drive fails you want to be able to continue operating without loss of data. [Guide to RAID for Dummies](https://tierradatarecovery.co.uk/dummies-guide-to-raid/)) 

**Keywords**

* Parity - extra info that can be used to recreate the data, if it.s lost

* Striping - splitting up data into different disks

* Stripe size - amount of data being read or written, to and from the disk at a time

**RAID0 **has striping, but no redundancy (doesn.t have mirroring or parity).



*   It.s fast because the data is split up into two hard drives.
*   If the drive fails, then you lose the data. (no redundancy)

**RAID1** has data mirroring, but no striping or parity. It.s meant to back up data.



*   Data is written to both drives.
*   If one drive fails, then you still have a backup.

**RAID5** has .block level striping. with distributed parity. It.s used primarily for redundancy, with some speed.



*   Needs 3 drives, minimum
*   Data is striped across the hard drives (like RAID0)
*   Stores some extra data so it knows how to reconstruct it if a drive fails

**RAID6** has two parity stripes on each .row.. Seems to be primarily for data redundancy.



*   Needs 4 drives, minimum
*   If both drives fails, then you can still recover your data.

Some additional documents about RAID: [Link](https://www.prepressure.com/library/technology/raid)
