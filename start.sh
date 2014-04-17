#! /bin/sh
sh ./ServerAgent-2.2.1/startAgent.sh &
python getmetrics.py output/metric_server_virtuoso.csv cpu:name=fuseki--network:bytessent--network:bytesrecv honegger &
apache-jmeter-2.11/bin/jmeter.sh -n -t "LDF eval.jmx"
python stopmetrics.py output/metric_server_virtuoso.csv
python parseclient.py "output/metric_client_*"
python parsebsbm.py "output/out_*.txt"