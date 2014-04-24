#!/bin/bash

# unmount possibly mounted drives
echo '=== unmounting drives ==='
sudo umount /mnt/s3 /mnt/drive1 /mnt/drive2 /mnt

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

# mount the ldf bucket from S3 to the /mnt/s3 directory (with ubuntu user!)
echo
echo '=== mounting s3 ldf storage ==='
s3fs -o uid=1000,gid=1000 ldf /mnt/s3/
