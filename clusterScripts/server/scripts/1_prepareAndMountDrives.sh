#!/bin/bash

# unmount mounted drives
echo '=== unmounting drives ==='
sudo umount /mnt

# format local instance drives to ext4
echo
echo '=== formatting drives ==='
sudo mkfs.ext4 /dev/xvdb
sudo mkfs.ext4 /dev/xvdc

# mount local drives to /mnt/drive. and assign permissions to the ubuntu user
echo
echo '=== mounting local drives ==='
sudo mount -o noatime,commit=600 /dev/xvdb /mnt/drive1
sudo mount -o noatime,commit=600 /dev/xvdc /mnt/drive2
sudo chown ubuntu:ubuntu /mnt/drive1
sudo chown ubuntu:ubuntu /mnt/drive2
