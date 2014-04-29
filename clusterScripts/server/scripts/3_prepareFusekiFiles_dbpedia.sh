#/bin/bash

# prepares datafiles for fuseki
echo 'Extracting fuseki data...'
mkdir -p /mnt/drive1/dataset/dbpedia/100M &&\
s3cmd get s3://ldf/dataset/dbpedia/100M/fuseki-dbpedia.tar.xz /mnt/drive2 &&\
tar xpJvf /mnt/drive2/fuseki-dbpedia.tar.xz -C /mnt/drive1/dataset/dbpedia/100M &&\
rm /mnt/drive2/fuseki-dbpedia.tar.xz
