#!/bin/bash

# 
host=${1}
port=${2}
url=${3}
proxy=${4}
proxyPort=${5}

# Test Not found 404
curl -i -x "${proxy}:${proxyPort}" -o proxyoutput404.txt "${host}:${port}/badurl"
# Test Not Modified 304
curl -i -x "${proxy}:${proxyPort}" -o proxyoutput304.txt --header 'If-Modified-Since: Sat, 20 Oct 2024 01:24:29 GMT' "${host}:${port}/${url}"
# Test Not Implemented 501
curl -i -x "${proxy}:${proxyPort}" -o proxyoutput501.txt -X POST "${host}:${port}/${url}"
# Test Bad resquest 400
curl -i -x "${proxy}:${proxyPort}" -o proxyoutput400.txt -X WRONG "${host}:${port}/${url}"
# Test OK 200 and when "if modified" is later than "last modified"
curl -i -x "${proxy}:${proxyPort}" -o proxyoutput200.txt --header 'If-Modified-Since: Sat, 18 Oct 2024 01:24:29 GMT' "${host}:${port}/${url}"