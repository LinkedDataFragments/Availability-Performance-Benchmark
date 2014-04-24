#!/bin/bash

jmProcess=$(ps -ef | grep jmeter | grep java | grep server | tr -s ' ' | cut -d ' ' -f 2 )

if [ -z "$jmProcess" ]
then
	echo 'starting JMeter server...'
	~/evaluation/apache-jmeter-2.11/bin/jmeter-server &
	disown -a
else
	echo "JMeter server already started with PID $jmProcess !"
fi
