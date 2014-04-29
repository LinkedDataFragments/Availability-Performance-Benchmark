#!/bin/bash

echo 'Extracting virtuoso db files from S3. This can take a while...'

# extract Virtuoso data files to instance drive 1
echo '=== preparing files on drive 1 ==='
s3cmd get s3://ldf/dataset/dbpedia/100M/virtuoso_drive1.tar.xz /mnt/drive2 &&\
tar xvJf /mnt/drive2/virtuoso_drive1.tar.xz -C /mnt/drive1 &&\
rm /mnt/drive2/virtuoso_drive1.tar.xz

echo '=== preparing files on drive 2 ==='
s3cmd get s3://ldf/dataset/dbpedia/100M/virtuoso_drive2.tar.xz /mnt/drive1 &&\
tar xvJf /mnt/drive1/virtuoso_drive2.tar.xz -C /mnt/drive2 &&\
rm /mnt/drive1/virtuoso_drive2.tar.xz
