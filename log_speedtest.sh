#!/bin/bash

# Directory to store logs
LOG_DIR="/home/pi/capturespeed/logs"
mkdir -p "$LOG_DIR"

# File name based on current date
TODAY=$(date '+%Y-%m-%d')
LOG_FILE="$LOG_DIR/speedtest_$TODAY.csv"

# Create file with headers if it doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    echo "Date,Time,Ping (ms),Download (Mbps),Upload (Mbps)" > "$LOG_FILE"
fi

# Run speedtest and extract values
result=$(speedtest --format=json)

# Parse values using jq
date_now=$(date '+%Y-%m-%d')
time_now=$(date '+%H:%M:%S')
ping=$(echo "$result" | jq '.ping.latency')
download=$(echo "$result" | jq '.download.bandwidth / 125000' | bc -l)
upload=$(echo "$result" | jq '.upload.bandwidth / 125000' | bc -l)

# Round to 2 decimals
download=$(printf "%.2f" "$download")
upload=$(printf "%.2f" "$upload")
ping=$(printf "%.1f" "$ping")

# Append to today's CSV file
echo "$date_now,$time_now,$ping,$download,$upload" >> "$LOG_FILE"

