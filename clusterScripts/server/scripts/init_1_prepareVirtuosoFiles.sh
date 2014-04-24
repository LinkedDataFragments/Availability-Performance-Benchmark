#/bin/bash

# prepares datafiles to be loaded into virtuoso
mkdir -p /mnt/drive1/dataset/bsbm/100M &&\
cd /mnt/drive1/dataset/bsbm/100M &&\
echo 'Splitting dataset into smaller parts...' &&\
xzcat /mnt/s3/dataset/bsbm/100M/dataset.nt.xz | split -l 2000000 --additional-suffix=.nt - dataset_ &&\
echo 'gzipping parts...' &&\
pigz -v -9 dataset* &&\
echo 'Done!'

