#! /bin/bash
BACKENDPROGRAM="virtuoso"
echo ---Starting benchmark $BACKENDPROGRAM >> ../output/timing.txt
date +"%s%3N" >> ../output/timing.txt
python getmetrics.py "../output/metric_server_$BACKENDPROGRAM.csv" "10.0.0.80" &
python getmetrics.py "../output/metric_cache_$BACKENDPROGRAM.csv" "10.0.0.122" &
./apache-jmeter-2.11/bin/jmeter -n -r -t "./LDF eval2.jmx"
python stopmetrics.py "../output/metric_server_$BACKENDPROGRAM.csv"
python stopmetrics.py "../output/metric_cache_$BACKENDPROGRAM.csv"
echo ---Stopping benchmark $BACKENDPROGRAM >> ../output/timing.txt
date +"%s%3N" >> ../output/timing.txt
python archiveoutput.py