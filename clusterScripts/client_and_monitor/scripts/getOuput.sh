#!/bin/bash

# read clients from clients.txt
clients=$(cat clients.txt)

for client in $clients
do
        echo "Getting output from [$client]"
        scp -ri /home/ubuntu/.ssh/ldfclient.pem $client:~/output/* ~/output/
done

