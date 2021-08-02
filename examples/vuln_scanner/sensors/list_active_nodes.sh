#!/bin/bash

TMP_OUTPUT_FILE="/tmp/tmp.actv_nds"
NETSTAT="/usr/sbin/netstat"
IFCONFIG="/sbin/ifconfig"
TARGET_FILE_PATH="/tmp/active_nodes"

default_inet=$($NETSTAT -nr -f inet|grep default|tr -s ' '|cut -d ' ' -f 4)
netmask=$(/sbin/ifconfig ${default_inet}|grep 'inet '|tr -s ' '|cut -d ' ' -f 4)
broadcast=$(/sbin/ifconfig ${defaultinet}|grep 'inet '|tr -s ' '|cut -d ' ' -f 6)
last_ip=$(echo $broadcast|cut -d'.' -f 4)
default_gw=$(/usr/sbin/netstat -nr -f inet|grep default|tr -s ' '|cut -d ' ' -f 2)
# list_active_nodes=$("nmap -T5 -sn i${default_gw}-${last_ip}|grep 'Host is up' -B 1|grep 'scan report'|awk '{print $NF}'|sed 's/(//g'|sed 's/)//g' > ${TARGET_FILE_PATH}'")
list_active_nodes=$(nmap -T5 -sn ${default_gw}-${last_ip}|grep 'Host is up' -B 1|grep 'scan report'|awk '{print $NF}'|sed 's/(//g'|sed 's/)//g')
echo $list_active_nodes > $TMP_OUTPUT_FILE
echo $list_active_nodes
