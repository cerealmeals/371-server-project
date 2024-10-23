from socket import *
from _thread import *
import threading
from HTTPfunctions import *

# create TCP connection
hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverPort = 8088
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind((hostname,serverPort))
serverSocket.listen(5)

print ('The server is ready to receive at ID:', IPAddr, 'and Port:', serverPort)

def mutil_thread(connectionSocket):
    # while True:
        
        response = connectionSocket.recv(2048).decode()
        # if len(response) <= 0:
        #     print('no data')
        #     break


        # split the response line by line
        lines_in_response = response.split('\n')

        # remove the \r off every line
        for i in range(len(lines_in_response)):
            print(lines_in_response[i])
            lines_in_response[i] = lines_in_response[i][:-1]
        

        # get the first line and decode
        words_in_request_line = lines_in_response[0].split(' ')
        command = words_in_request_line[0]
        url = words_in_request_line[1]
        version = words_in_request_line[2]
        

        print("RESPONSE:")
        match command:
            case 'GET':
                GetCommand(lines_in_response, version, connectionSocket, url, IPAddr, serverPort)
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
        connectionSocket.close()


while True:
    connectionSocket, addr = serverSocket.accept()
    
    # sentence = connectionSocket.recv(1024).decode()
    # capitalizedSentence = sentence.upper()
    # connectionSocket.send(capitalizedSentence.encode())

    # client acquire the lock
    print('address:', addr[0], ':', addr[1])

    # open a new thread
    start_new_thread(mutil_thread,(connectionSocket,))
    # connectionSocket.close()

serverSocket.close()