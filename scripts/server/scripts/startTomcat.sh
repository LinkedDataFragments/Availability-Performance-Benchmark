#!/bin/bash

# first check if temporary dirs (logging, tmp, ...) exist
if [ ! -e "/mnt/drive1/tomcat_tmp" ]
then
	echo 'creating Tomcat temporary output directory /mnt/drive1/tomcat_tmp'
	mkdir -p /mnt/drive1/tomcat_tmp/tmp
	mkdir /mnt/drive1/tomcat_tmp/logs

fi

export CATALINA_HOME=/home/ubuntu/progs/apache-tomcat-7.0.53
$CATALINA_HOME/bin/catalina.sh start
