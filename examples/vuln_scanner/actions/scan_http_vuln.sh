#!/bin/bash

FILE_DIR=$(dirname "${BASH_SOURCE[0]}")
OUTPUT_DIR="/tmp"
SENSORS_DIR="$FILE_DIR/../sensors"
ACTIVE_HTTP_FILE="/tmp/tmp.actv_http"
if [ ! -f $ACTIVE_HTTP_FILE ]; then
    exec $SENSORS_DIR/active_http_servers.sh
fi

for host in `cat $ACTIVE_HTTP_FILE`; do
    nikto -host $host > $OUTPUT_DIR/tmp.nikto_$host
done