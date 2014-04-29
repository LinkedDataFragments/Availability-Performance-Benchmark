#/bin/bash

# prepares datafiles to be loaded into virtuoso
echo 'Retrieving dataset file from S3...'
s3cmd get s3://ldf/dataset/dbpedia/100M/dataset.nt.xz /mnt/drive2 &&\
mkdir -p /mnt/drive1/dataset/dbpedia/100M &&\
cd /mnt/drive1/dataset/dbpedia/100M &&\
echo 'Splitting dataset into smaller parts...' &&\
xzcat /mnt/drive2/dataset.nt.xz | split -l 2000000 --additional-suffix=.nt - dataset_ &&\
rm /mnt/drive2/dataset.nt.xz &&\
echo 'gzipping parts...' &&\
pigz -v -9 dataset* &&\
echo 'Done!'

