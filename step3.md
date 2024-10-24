a)  A proxy server needs to be able to receive HTTP requests and redirect them 
    to the correct destination get the response from the correct server and 
    return that response to the original client.

    If the cache of the proxy server does not have the data which the client requested, The proxy server will fetch 
    the hostname and port number from the client's request and create a socket connection with the web server, then send 
    the request from the client to the web server. Then the web server will handle the request and send response and requested 
    data back to proxy server, then the proxy server will send the response and requested data back to client.
    If the reponse from the web server is 200 OK, then the proxy server will cache the data. If other clients request for the 
    data that is in the cache, the proxy server will not send requests to the web server, instead, it will find the data 
    in the cache and handle client's request, then send back response and requested data back to the server

b)  



c)  We initially created the server single threaded and then implement multi-threaded.
    But quickly changed it beacuse the server needs to be able to respond to multiple clients at a time.
    When you accept a connecting you make a thread to handle the connection when that specific connection ends
    you close the connection and the thread.
    Being multithreaded alows for better performance because at some points your server might be waiting for the client,
    during that time it can service other clients but only if it is multithreaded. It also allows the server to be almost
    continuouly accepting new connections from clients. Our server has a max backlog of clients to be connected of 5.