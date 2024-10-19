from socket import *
import datetime
import os


def GetCommand(lines_in_response, version, connectionSocket, url):

    host = 'error'
    for line in lines_in_response:
        #print(line)
        if line[:6] == 'Host: ':
            host = line[6:]
    #print(host)

    if(host != (IPAddr + ':'+ str(serverPort))):
        #proxy server stuff
        BadRequest(version, connectionSocket)
        return True
    
    url = url[1:]
    try:
        f = open(url, 'r', encoding='utf-8')
        try:
            data = f.read()
        except Exception as e:
            print(e)
            BadRequest(version, connectionSocket)
            f.close()
            return True
    except Exception as e:
        print(e)
        NotFound(version, connectionSocket)
        return True
    f.close()
    
    response_lines = []
    response_lines.append(version + ' 200 OK')
    date = datetime.datetime.now()
    response_lines.append('Date: ' + date.strftime("%c"))
    response_lines.append('Server: ' + IPAddr)
    response_lines.append('Accept-Ranges: bytes')
    response_lines.append('Content-Length: ' + str(len(data.encode('utf-8'))))
    response_lines.append('')
    response_lines.append(data)
    to_send = '\r\n'.join(response_lines)

    print(to_send)
    connectionSocket.send(to_send.encode())
    return False
    


def NotImplmented(version, connectionSocket):
    to_send = version + ' 501 Not Implemented'
    print(to_send)
    connectionSocket.send(to_send.encode())

def BadRequest(version, connectionSocket):
    to_send = version + ' 400 Bad request'
    print(to_send)
    connectionSocket.send(to_send.encode())

def NotFound(version, connectionSocket):
    to_send = version + ' 404 Not Found'
    print(to_send)
    connectionSocket.send(to_send.encode())


# TODO
def NotModified(version, connectionSocket):
    print('TODO')
    raise Exception('Not Implemented')
    to_send = version + ' 304 Not modified'
    print(to_send)
    connectionSocket.send(to_send.encode())


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

    # split the response line by line
    lines_in_response = response.split('\n')

    # remove the \r off every line
    for i in range(len(lines_in_response)):
        lines_in_response[i] = lines_in_response[i][:-1]
    

    # get the first line and decode
    words_in_request_line = lines_in_response[0].split(' ')
    command = words_in_request_line[0]
    url = words_in_request_line[1]
    version = words_in_request_line[2]
    

    print("RESPONSE:")
    match command:
        case 'GET':
            flag = GetCommand(lines_in_response, version, connectionSocket, url)
        case 'HEAD':
            NotImplmented(version, connectionSocket)
        case 'POST':
            NotImplmented(version, connectionSocket)
        case 'PUT':
            NotImplmented(version, connectionSocket)
        case 'DELETE':
            NotImplmented(version, connectionSocket)
        case 'CONNECT':
            NotImplmented(version, connectionSocket)
        case 'OPTIONS':
            NotImplmented(version, connectionSocket)
        case 'TRACE':
            NotImplmented(version, connectionSocket)
        case 'PATCH':
            NotImplmented(version, connectionSocket)
        case _: # Should be bad request because not a normal command
            BadRequest(version, connectionSocket)
    connectionSocket.close()


