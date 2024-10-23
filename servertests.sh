#!/bin/bash

# 
host=${1}
port=${2}
url=${3}

# Test Not found 404
curl -i -o output404.txt "${host}:${port}/badurl"
# Test Not Modified 304
curl -i -o output304.txt --header 'If-Modified-Since: Sat, 20 Oct 2024 01:24:29 GMT' "${host}:${port}/${url}"
# Test Not Implemented 501
curl -i -o output501.txt -X POST "${host}:${port}/${url}"
# Test Bad resquest 400
curl -i -o output400.txt -X WRONG "${host}:${port}/${url}"
# Test OK 200 and when "if modified" is later than "last modified"
curl -i -o output200.txt --header 'If-Modified-Since: Sat, 18 Oct 2024 01:24:29 GMT' "${host}:${port}/${url}"

