# Step One: Determine Requirements

1. 200	OK
Requirements: 
    a. use GET method
    b. the requested file exists on the server
    c. the protocol is "HTTP/1.1"

Message part: 
    the request line 
    e.g. GET /test.html HTTP/1.1\r\n
    command + url + version

Test HTTP request:
    GET /test.html HTTP/1.1\r\n
    Host: localhost:8088\r\n

2. 304	Not Modified
Requirements: 
        a. there is "If-Modified-Since" message in the header file
        b. the requested file exists on the server
        c. compare the time in the header file and the last modified time from the file
        if the time from the header >= file last modified time, then it is not modified

Message part: 
    in the header file, the line starts with "If-Modified-Since", and with a time

Test HTTP request:
    GET /test.html HTTP/1.1\r\n
    Host: localhost:8088\r\n
    If-Modified-Since: Tue, 14 Oct 2024 10:00:00 GMT\r\n\r\n

3. 400	Bad request
Requirements: 
    a. malformed request syntax (the number of elements in the request line is not 3)
    b. invalid request message framing 
    c. the protocol is not "HTTP/1.1"

Message part: 
    the request line 
    e.g. GET /test.html HTTP/1.1\r\n
    command + url + version

Test HTTP request:
    GET /test.html HTTP/1.0\r\n
    Host: localhost:8088\r\n

4. 404	Not Found
Requirements: 
    the requested file does not exist on the server

Message part: 
    the url in the request line

Test HTTP request:
    GET /notExist.html HTTP/1.1\r\n
    Host: localhost:8088\r\n

5. 501	Not Implemented
Requirements: 
    the method is not GET

Message part: 
    the first element in the request line (command)

Test HTTP request:
    POST /test.html HTTP/1.1\r\n
    Host: localhost:8088\r\n
    