from socket import *
import threading

# extract host and port
def extract_host_and_port(request):
    # find return the index of the beginning of 'Host:', plus the length so it's the index of 
    # the start of host
    host_start = request.find(b'Host: ') + len(b'Host: ')

    # search starts from: host_start
    host_end = request.find(b'\r\n', host_start)

    # extract the host info
    host_data = request[host_start:host_end].decode('utf-8')
    # print(host_data)
    get_hostname_position = host_data.find("/")
    port_position = host_data.find(":")

    port = int((host_data[(port_position + 1):])) 
    host = host_data[:port_position]

    return host, port

# read data from client requests
def handle_client_request(client_socket):
    print("received request: \n")

    # byte object
    request = b''
    
    while True:
        message = client_socket.recv(1024)

        if len(message) > 0:
            request += message
            print(message.decode('utf-8'))
            if b'\r\n\r\n' in request:
                break
        else:
            break

    # extract web server's host and port from the request
    host, port = extract_host_and_port(request)
    # print("host:", host)
    # print("port:", port)
    # create a socket to connect to the destination server
    dest_socket = socket(AF_INET, SOCK_STREAM)
    dest_socket.connect((host, port)) 

    # send the request to the original server
    dest_socket.sendall(request)

    print("received response: \n")

    while True:
        # get response from the original server
        response = dest_socket.recv(1024)
        print(response.decode('utf-8'))
        if len(response) > 0:
            client_socket.sendall(response)
        else:
            print("line62")
            break

    dest_socket.close()
    client_socket.close()

# accept client requests
hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverPort = 8214
serverSocket = socket(AF_INET, SOCK_STREAM)
#proxy_host = '127.0.0.1'
serverSocket.bind((hostname, serverPort))
serverSocket.listen(5)

print('Proxy Server is ready at IP:', IPAddr, ' and port:', serverPort)
while True:
    client_socket, addr = serverSocket.accept()
    print('address:', addr[0], ':', addr[1])

    # create a thread for handling the client request
    handle_client = threading.Thread(target=handle_client_request, args=(client_socket,))
    handle_client.start()  


