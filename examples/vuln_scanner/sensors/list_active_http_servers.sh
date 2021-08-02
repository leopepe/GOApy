#!/bin/bash
# the script returns "true" when the list of active nodes
# are different than the prevous one

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

# check if the output is different from previous list
cmp -s <(echo ${result[@]}) <(cat $TMP_OUTPUT_FILE)
if [ $? -eq 1 ]; then
    printf "false"
    exit 0
else
    @echo ${result[@]} > $TMP_OUTPUT_FILE
    # echo ${result[@]}
    printf "true"
    exit 0
fi