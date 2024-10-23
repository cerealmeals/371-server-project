from socket import *
from time import gmtime, strftime, strptime
import os
from calendar import timegm


def makeHTTPresponse(statusLine, data, url, IPAddr):

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

def GetCommand(lines_in_response, version, connectionSocket, url, IPAddr, serverPort):
    
    # get the url
    if url.find('https://') != -1:
        start = url.find('https://') + len('https://')
        url = url[1 + url.find('/',start):]
    elif url.find('http://') != -1:
        start = url.find('http://') + len('http://')
        url = url[1 + url.find('/',start + 1):]
    else:
        url = url[1:]

    host = 'error'
    for line in lines_in_response:
        #print('test', line)
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
    
    # try to open the file
    try:
        f = open(url, 'r', encoding='utf-8')
        try:
            data = f.read()
        except Exception as e:
            print(e)
            BadRequest(version, connectionSocket, IPAddr)
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
    


def NotImplmented(version, connectionSocket, IPAddr):
    to_send = makeHTTPresponse(version + ' 501 Not Implemented', None, None, IPAddr)
    print(to_send)
    connectionSocket.send(to_send.encode())

def BadRequest(version, connectionSocket, IPAddr):
    to_send = makeHTTPresponse(version + ' 400 Bad request', None, None, IPAddr)
    print(to_send)
    connectionSocket.send(to_send.encode())

def NotFound(version, connectionSocket, IPAddr):

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

    to_send = makeHTTPresponse(version + ' 404 Not Found', data, '404.html', IPAddr)
    print(to_send)
    connectionSocket.send(to_send.encode())



def NotModified(version, connectionSocket, url, IPAddr):
    
    to_send = makeHTTPresponse(version + ' 304 Not modified', None, url, IPAddr)
    print(to_send)
    connectionSocket.send(to_send.encode())
