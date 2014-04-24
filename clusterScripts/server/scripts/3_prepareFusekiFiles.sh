#/bin/bash

# prepares datafiles for fuseki
echo 'Extracting fuseki data...'
mkdir -p /mnt/drive2/dataset/bsbm/100M &&\
tar xpJvf /mnt/s3/dataset/bsbm/100M/fuseki-bsbm.tar.xz -C /mnt/drive2/dataset/bsbm/100M

