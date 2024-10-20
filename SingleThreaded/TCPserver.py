from socket import *
from time import gmtime, strftime, strptime
import os
from calendar import timegm


def makeHTTPresponse(statusLine, data, url):

    response_lines = []
    response_lines.append(statusLine)
    response_lines.append('Date: ' + strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))
    if url != None:
        response_lines.append('Last-Modified: ' + strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime(os.path.getmtime(url))))
    response_lines.append('Server: ' + IPAddr)
    if data != None:
        response_lines.append('Accept-Ranges: bytes')
        response_lines.append('Content-Length: ' + str(len(data.encode('utf-8'))))
    response_lines.append('')
    if data != None:
        response_lines.append(data)
    to_send = '\r\n'.join(response_lines)
    return to_send

def GetCommand(lines_in_response, version, connectionSocket, url):
    url = url[1:]
    host = 'error'
    for line in lines_in_response:
        #print('test', line)
        if line[:6] == 'Host: ':
            host = line[6:]
        elif line[:19] == 'If-Modified-Since: ':
            t_string = line[19:(19+25)]
            #print(t_string)
            if os.path.getmtime(url) < timegm(strptime(t_string, '%a, %d %b %Y %H:%M:%S')):
                NotModified(version, connectionSocket, url)
                return True
    #print(host)

    if(host != (IPAddr + ':'+ str(serverPort))):
        #proxy server stuff
        BadRequest(version, connectionSocket)
        return True
    

    #print(url)
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
    
    
    to_send = makeHTTPresponse(version + ' 200 OK', data, url)

    print(to_send)
    connectionSocket.send(to_send.encode())
    return False
    


def NotImplmented(version, connectionSocket):
    to_send = makeHTTPresponse(version + ' 501 Not Implemented', None, None)
    print(to_send)
    connectionSocket.send(to_send.encode())

def BadRequest(version, connectionSocket):
    to_send = makeHTTPresponse(version + ' 400 Bad request', None, None)
    print(to_send)
    connectionSocket.send(to_send.encode())

def NotFound(version, connectionSocket):

    try:
        f = open('404.html', 'r', encoding='utf-8')
        try:
            data = f.read()
        except Exception as e:
            print(e)
            f.close()
            return True
    except Exception as e:
        print(e)
        return True
    f.close()

    to_send = makeHTTPresponse(version + ' 404 Not Found', data, '404.html')
    print(to_send)
    connectionSocket.send(to_send.encode())



def NotModified(version, connectionSocket, url):
    
    to_send = makeHTTPresponse(version + ' 304 Not modified', None, url)
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


