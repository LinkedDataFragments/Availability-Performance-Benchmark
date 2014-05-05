#!/bin/bash

jmProcess=$(ps -ef | grep ServerAgent | grep 2.2.1 | tr -s ' ' | cut -d ' ' -f 2 )

if [ -z "$jmProcess" ]
then
	echo 'starting Server agent...'
	~/evaluation/ServerAgent-2.2.1/startAgent.sh > /tmp/serveragent.log 2>&1 &
	disown -a
else
	echo "Server agent already started with PID $jmProcess !"
fi
