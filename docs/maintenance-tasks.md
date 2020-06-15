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

Scrub checks the file system's integrity, and repairs any issues that it finds. After the scrub is finished, it is good to also run `zpool status` to check if there is anything wrong.

