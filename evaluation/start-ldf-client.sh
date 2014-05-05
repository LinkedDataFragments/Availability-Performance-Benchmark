#!/bin/bash

jmProcess=$(ps -ef | grep ldf | grep node | tr -s ' ' | cut -d ' ' -f 2 )

if [ -z "$jmProcess" ]
then
	echo 'starting LDF client...'
	nodejs ~/evaluation/client/bin/ldf-client-http ~/evaluation/config-client.json > /tmp/ldfclient.log 2>&1 &
	disown -a
else
	echo "JMeter server already started with PID $jmProcess !"
fi
