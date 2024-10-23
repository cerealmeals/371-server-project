from socket import *
from _thread import *
import threading
from HTTPfunctions import *

# accept client requests
hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverPort = 8234
serverSocket = socket(AF_INET, SOCK_STREAM)
#proxy_host = '127.0.0.1'
serverSocket.bind((hostname, serverPort))
serverSocket.listen(5)

print('Proxy Server is ready at IP:', IPAddr, ' and port:', serverPort)


# extract host and port
def extract_host_and_port(request):
    # find return the index of the beginning of 'Host:', plus the length so it's the index of 
    # the start of host
    host_start = request.find('Host: ') + len('Host: ')

    # search starts from: host_start
    host_end = request.find('\r\n', host_start)

    # extract the host info
    host_data = request[host_start:host_end]
    # print(host_data)
    get_hostname_position = host_data.find("/")
    port_position = host_data.find(":")

    port = int((host_data[(port_position + 1):])) 
    host = host_data[:port_position]

    return host, port

def GetCommand_cache(lines_in_response, version, connectionSocket, url, IPAddr, serverPort):
    
    # get the url
    # if url.find('https://') != -1:
    #     start = url.find('https://') + len('https://')
    #     url = url[1 + url.find('/',start):]
    # elif url.find('http://') != -1:
    #     start = url.find('http://') + len('http://')
    #     url = url[1 + url.find('/',start + 1):]
    # else:
    #     url = url[1:]
    print("line35", url)
    
    host = 'error'
    for line in lines_in_response:
        print('test', line)
        if line[:6] == 'Host: ':
            host = line[6:]
            if(host != (IPAddr + ':'+ str(serverPort))):
                #proxy server stuff
                BadRequest(version, connectionSocket, IPAddr)
                return True
        elif line[:19] == 'If-Modified-Since: ':
            t_string = line[19:(19+25)]
            #print(t_string)
            if os.path.getmtime(url) < timegm(strptime(t_string, '%a, %d %b %Y %H:%M:%S')):
                NotModified(version, connectionSocket, url, IPAddr)
                return True
    
    # if the host line is not there send bad request
    if host == 'error':
        BadRequest(version, connectionSocket, IPAddr)
    
    # try to open the file
    try:
        f = open(url, 'r', encoding='utf-8')
        try:
            data = f.read()
        except Exception as e:
            print(e)
            f.close()
            return True
    except Exception as e:
        print(e)
        NotFound(version, connectionSocket, IPAddr)
        return True
    f.close()
    
    
    to_send = makeHTTPresponse(version + ' 200 OK', data, url, IPAddr)

    print(to_send)
    connectionSocket.send(to_send.encode())
    return False
    
def send_from_caching(lines_in_response, version, connectionSocket, url, IPAddr, serverPort, command):
    print("line 40", version)
    print("line 41", url)
    match command:
            case 'GET':
                GetCommand_cache(lines_in_response, version, connectionSocket, url, IPAddr, serverPort)
            case 'HEAD':
                NotImplmented(version, connectionSocket, IPAddr)
            case 'POST':
                NotImplmented(version, connectionSocket, IPAddr)
            case 'PUT':
                NotImplmented(version, connectionSocket, IPAddr)
            case 'DELETE':
                NotImplmented(version, connectionSocket, IPAddr)
            case 'CONNECT':
                NotImplmented(version, connectionSocket, IPAddr)
            case 'OPTIONS':
                NotImplmented(version, connectionSocket, IPAddr)
            case 'TRACE':
                NotImplmented(version, connectionSocket, IPAddr)
            case 'PATCH':
                NotImplmented(version, connectionSocket, IPAddr)
            case _: # Should be bad request because not a normal command
                BadRequest(version, connectionSocket, IPAddr)

# read data from client requests
def handle_client_request(client_socket):
    print("received request: \n")

    # byte object
    #request = b''
    
    while True:
        request = client_socket.recv(2048).decode('utf-8')

        if len(request) > 0:
            #request += message
            #print(message.decode('utf-8'))
            print(request)
            if '\r\n\r\n' in request:
                break
        else:
            break

    # get the url
    # split the response line by line
    lines_in_response = request.split(os.linesep)
        
    # get the first line and decode
    words_in_request_line = lines_in_response[0].split(' ')
    command = words_in_request_line[0]
    url = words_in_request_line[1]
    version = words_in_request_line[2]

    # get the url
    if url.find('https://') != -1:
        start = url.find('https://') + len('https://')
        url = url[1 + url.find('/',start):]
    elif url.find('http://') != -1:
        start = url.find('http://') + len('http://')
        url = url[1 + url.find('/',start + 1):]
    else:
        url = url[1:]
    
    print("line158", url)

    try:
        f = open(url, 'r', encoding='utf-8') 
        print("line 104")
        send_from_caching(lines_in_response, version, client_socket, url, IPAddr, serverPort, command)
    except Exception as e:

        # extract web server's host and port from the request
        host, port = extract_host_and_port(request)
        # print("host:", host)
        # print("port:", port)
        # create a socket to connect to the destination server
        dest_socket = socket(AF_INET, SOCK_STREAM)
        dest_socket.connect((host, port)) 

        # send the request to the original server
        dest_socket.sendall(request.encode())

        print("received response: \n")


        while True:
            # get response from the original server
            response = dest_socket.recv(2048).decode('utf-8')

            print(response)
            if len(response) > 0:
                client_socket.sendall(response.encode())

                # store the file in the cache, create a html file which the name is the same as in the url but before the ".html" part
                # print("line184", url)
                cache_file_name = url
                file_stream = open(cache_file_name,"w") 

                # fetch the html part from the response
                start = response.find('<!DOCTYPE html>') 
                context = response[start:]

                # write html to a html file??
                file_stream.write(context)

                file_stream.close()
            else:
                print("line62")
                break

        dest_socket.close()

    client_socket.close()


while True:
    client_socket, addr = serverSocket.accept()
    print('address:', addr[0], ':', addr[1])

    # create a thread for handling the client request
    handle_client = threading.Thread(target=handle_client_request, args=(client_socket,))
    handle_client.start()  
    # start_new_thread(handle_client_request,(client_socket,))
