#! /bin/bash
BACKENDPROGRAM="virtuoso"
python getmetrics.py "../output/metric_server_$BACKENDPROGRAM.csv" "10.0.0.244" &
./apache-jmeter-2.11/bin/jmeter -n -r -t "./LDF eval2.jmx"
python stopmetrics.py "../output/metric_server_$BACKENDPROGRAM.csv"
python archiveoutput.py