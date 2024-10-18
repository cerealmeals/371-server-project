#!/bin/bash


host=${1}
port=${2}
# telnet $host $port << EOF
# GET url HTTP/1.1
# EOF
# sleep 1

# echo "open ${host} ${port}" 
# sleep 1
# echo "GET /test.html HTTP/1.1" 
# echo "Host: sfu.ca"
# echo
# sleep 2

curl '${host}:${port}'

