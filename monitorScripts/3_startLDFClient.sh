#!/bin/bash

# read clients from clients.txt
clients=$(cat clients.txt)

for client in $clients
do  
  echo "Starting LDFclient on [$client], if not running yet."
	ssh -i /home/ubuntu/.ssh/ldfclient.pem $client '/home/ubuntu/evaluation/start-ldf-client.sh'
done
