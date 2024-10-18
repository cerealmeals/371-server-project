from socket import *

hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverPort = 8081
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind((hostname,serverPort))
serverSocket.listen(1)

print ('The server is ready to receive at IP address:', IPAddr, 'and port:', serverPort)
flag = True
while flag:
    connectionSocket, addr = serverSocket.accept()
    # multi threaded you make a new thread to do everything below this
    response = connectionSocket.recv(2048).decode()

    
    lines_in_response = response.split('\n')
    print('Whole response:','\n'+response, '\nEND OF WHOLE RESPONSE')
    print(lines_in_response)
    words_in_request_line = lines_in_response[0].split(' ')
    command = words_in_request_line[0]
    url = words_in_request_line[1]
    version = words_in_request_line[2]
    print('version:', version)
    # last_in_list = len(words_in_request_line)-1

    # R_char_and_L_char = words_in_request_line[last_in_list][-2:]
    # print(R_char_and_L_char)
    # if(R_char_and_L_char == '\n'):
    #     print('yassss')

    print("RESPONSE:")
    match command:
        case 'GET':
            to_send = (version + ' 200 OK')
            print(version)
            print(to_send)
            connectionSocket.send(to_send.encode())
            flag = False
        case 'HEAD':
            to_send = version + ' Not Implemented'
            print(to_send)
            connectionSocket.send(to_send.encode())
        case _: # Should be bad request because not a normal command
            to_send = version + ' Bad request'
            print(to_send)
            connectionSocket.send(to_send.encode())
    connectionSocket.close()