#/bin/bash

echo 'Deleting previous fuseki files'
rm -rf /mnt/drive1/dataset/*
rm -rf /mnt/drive2/dataset/*

# prepares datafiles for fuseki
echo 'Extracting fuseki data...'
mkdir -p /mnt/drive1/dataset/sp2b/100M &&\
s3cmd get s3://ldf/dataset/sp2b/100M/fuseki-sp2b.tar.xz /mnt/drive2 &&\
tar xpJvf /mnt/drive2/fuseki-sp2b.tar.xz -C /mnt/drive1/dataset/sp2b/100M &&\
rm /mnt/drive2/fuseki-sp2b.tar.xz
