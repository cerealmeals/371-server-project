from socket import *

hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverPort = 8080
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind((hostname,serverPort))
serverSocket.listen(1)

print ('The server is ready to receive')
flag = True
while flag:
    connectionSocket, addr = serverSocket.accept()
    # multi threaded you make a new thread to do everything below this
    response = connectionSocket.recv(2048).decode()

    print('Whole response:\n',response, '\nEND OF WHOLE RESPONSE')
    lines_in_response = response.split('\n')
    words_in_request_line = lines_in_response[0].split(' ')
    command = words_in_request_line[0]
    version = words_in_request_line[2]

    last_in_list = len(words_in_request_line)-1

    R_char_and_L_char = words_in_request_line[last_in_list][-2:]
    print(R_char_and_L_char)
    if(R_char_and_L_char == '\n'):
        print('yassss')
    match command:
        case 'GET':
            print('http version:', version)
            to_send = version + ' 200 OK'
            connectionSocket.send(to_send.encode())
            flag = False
        case 'HEAD':
            connectionSocket.send('Not Implemented'.encode())
        case _: # Should be bad request because not a normal command
            connectionSocket.send('Bad request'.encode())
    connectionSocket.close()