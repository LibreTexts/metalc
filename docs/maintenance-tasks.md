# Maintenance Tasks

This document lists all tasks that should be done regularly.

## Security Update on Rooster

* Frequency: weekly
* Command: `sudo unattended-upgrade -d`

Rooster is the only server that has a public network. It is essential to keep the system up to date. We use [unattended-upgrade](https://github.com/mvo5/unattended-upgrades) to upgrade packages safely. To minimize affecting the cluster, check the following before running the command:

1. Run `sudo unattended-upgrade -d --dry-run` to make sure that it will upgrade without error.
2. Check `kubectl get pods -n jhub` to see if there are a lot of people using the cluster. Try to upgrade when no one is there.

Additionally, there is a cron job on rooster that runs `sudo unattended-upgrade -d --dry-run` and sends out weekly emails on Friday. Do `sudo crontab -e` to edit the cron job. If you wish to change the code of the cron job, the shell script is located at `/home/spicy/metalc-configurations/cronjob/weekly-security-update`. The shell script is a python script that uses pipes to run commands.

## Scrub Checks on Hen (ZFS)

* Frequency: monthly
* Command: `sudo zpool scrub nest`

To execute manually, you must first ssh into hen from rooster with the command `ssh hen`. Scrub checks the file system's integrity, and repairs any issues that it finds. After the scrub is finished, it is good to also run `zpool status` to check if there is anything wrong.

This command is run on a cronjob, so there should be no need for manual intervention. The cronjob runs at 8:00AM the first day of every month. Rooster will also send out an email at 8:10AM on the same day with the results. If the scrub is fine, the email should be titled `[All clear] Hen monthly ZFS report`. If the title says `[POTENTIAL ZFS ISSUE]` instead, there may be something wrong with the disk, and the email contains the `zpool status` output which you can use to debug disk issues. Details on how the cronjob is setup are in the private configuration repo, under `cronjob/monthly-zfs-report.py`.
