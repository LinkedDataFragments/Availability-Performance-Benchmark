#! /bin/bash
./ServerAgent-2.2.1/startAgent.sh --auto-shutdown &
python getmetrics.py "../output/metric_server_virtuoso.csv" "cpu:name=virtuoso--network:bytessent--network:bytesrecv" "ec2-54-86-22-42.compute-1.amazonaws.com" &
./apache-jmeter-2.11/bin/jmeter -n -t "./LDF eval2.jmx"
python stopmetrics.py "../output/metric_server_virtuoso.csv"
python parseclient.py "../output/metric_client_*.csv"
python parsebsbm.py "../output/out_*.txt"