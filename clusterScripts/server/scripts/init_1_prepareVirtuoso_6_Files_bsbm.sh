#/bin/bash

# prepares datafiles to be loaded into virtuoso
echo 'Retrieving dataset file from S3...'
s3cmd get s3://ldf/dataset/bsbm/100M/dataset.nt.xz /mnt/drive2 &&\
mkdir -p /mnt/drive1/dataset/bsbm/100M &&\
cd /mnt/drive1/dataset/bsbm/100M &&\
echo 'Converting dataset to gzipped file...' &&\
xzcat /mnt/drive2/dataset.nt.xz | pigz -9 > dataset.nt.gz &&\
rm /mnt/drive2/dataset.nt.xz &&\
echo 'Done!'

