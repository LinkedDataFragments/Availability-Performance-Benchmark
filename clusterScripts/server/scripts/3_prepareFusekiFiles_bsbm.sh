#/bin/bash

echo 'Deleting previous fuseki files'
rm -rf /mnt/drive1/dataset/*
rm -rf /mnt/drive2/dataset/*

# prepares datafiles for fuseki
echo 'Extracting fuseki data...'
mkdir -p /mnt/drive2/dataset/bsbm/100M &&\
s3cmd get s3://ldf/dataset/bsbm/100M/fuseki-bsbm.tar.xz /mnt/drive1 &&\
tar xpJvf /mnt/drive1/fuseki-bsbm.tar.xz -C /mnt/drive2/dataset/bsbm/100M &&\
rm /mnt/drive1/fuseki-bsbm.tar.xz
