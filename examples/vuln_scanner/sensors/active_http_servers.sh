#!/bin/bash

FILE_DIR=$(dirname "${BASH_SOURCE[0]}")
TMP_OUTPUT_FILE="/tmp/tmp.actv_http"
ACTIVE_NODES_FILE="/tmp/tmp.actv_nds"
if [ ! -f $ACTIVE_NODES_FILE ]; then
    exec $FILE_DIR/list_active_nodes.sh
fi

for node in `cat $ACTIVE_NODES_FILE`; do 
    ip=`/usr/bin/nc -zn $node 80 2>&1 | grep succeeded|cut -d" " -f3`
    result=(${result[@]} $ip)
done

echo ${result[@]} > $TMP_OUTPUT_FILE
echo ${result[@]}