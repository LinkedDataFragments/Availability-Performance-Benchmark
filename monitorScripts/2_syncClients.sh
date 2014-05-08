#!/bin/bash

# read clients from clients.txt
clients=$(cat clients.txt)

for client in $clients
do
	echo "syncing [$client]"
	rsync --rsh='ssh -o StrictHostKeyChecking=no -i /home/ubuntu/.ssh/ldfclient.pem' -rav ~/evaluation $client:~/

	echo "Starting jmeter on [$client], if not running yet."
	ssh -i /home/ubuntu/.ssh/ldfclient.pem $client 'mkdir output; /home/ubuntu/evaluation/start-jmeter-server.sh'
  
  echo "Starting serverAgent on [$client], if not running yet."
	ssh -i /home/ubuntu/.ssh/ldfclient.pem $client '/home/ubuntu/evaluation/start-serveragent.sh'
done
