#!/bin/bash

jmProcess=$(ps -ef | grep java | grep ldf | grep jena | tr -s ' ' | cut -d ' ' -f 2 )

if [ -z "$jmProcess" ]
then
	echo 'starting LDF client...'
	java -jar ~/evaluation/client/ldf-jena-http-1.0-SNAPSHOT-jar-with-dependencies.jar ~/evaluation/config-client.json 3000 > /tmp/ldfjenaclient.log 2>&1 &
	disown -a
else
	echo "JMeter server already started with PID $jmProcess !"
fi
