#! /bin/bash
BACKENDPROGRAM="virtuoso"
echo ---Starting benchmark $BACKENDPROGRAM >> timing.txt
date +"%s" >> timing.txt
python getmetrics.py "../output/metric_server_$BACKENDPROGRAM.csv" "10.0.0.80" &
./apache-jmeter-2.11/bin/jmeter -n -r -t "./LDF eval2.jmx"
python stopmetrics.py "../output/metric_server_$BACKENDPROGRAM.csv"
echo ---Stopping benchmark $BACKENDPROGRAM >> timing.txt
date +"%s" >> timing.txt
python archiveoutput.py