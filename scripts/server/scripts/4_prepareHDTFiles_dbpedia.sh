#/bin/bash

echo 'Deleting previous HDT files'
rm -rf /mnt/drive1/hdt

# prepares datafiles for HDT
echo 'Extracting HDT data...'
mkdir -p /mnt/drive1/hdt &&\
s3cmd get s3://ldf/dataset/dbpedia/100M/dataset.hdt.xz /mnt/drive1/hdt &&\
s3cmd get s3://ldf/dataset/dbpedia/100M/dataset.hdt.index.xz /mnt/drive1/hdt &&\
unxz -v /mnt/drive1/hdt/dataset.hdt.xz &&\
unxz -v /mnt/drive1/hdt/dataset.hdt.index.xz
