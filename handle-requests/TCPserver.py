from socket import *
from _thread import *
import threading

# create TCP connection
hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverPort = 8088
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind((hostname,serverPort))
serverSocket.listen(5)

print ('The server is ready to receive')

# muti-threading
thread_lock = threading.Lock()

def mutil_thread(connectionSocket):
    while True:
        message = connectionSocket.recv(1024).decode()
        if not message:
            print('no data')
            thread_lock.release()
            break

        print(message)

        # handle HTTP GET requests

        # case 1: 400 Bad request
        # the number of elements of the request line is not 3
        # or the protocol is not 'http 1.1'

        # case 2: 501 Not Implemented
        # if it's not GET, return 501

        # case 3: 404 Not Found
        # if the file does not exist, return 404
        # can't open the 'test.html'

        # case 4: 304 Not Modified
        # if there is "If-Modified-Since" message in the header file
        # AND compare the time in the header file and the modified time from the file
        # os.path.getmtime(path) "The method returns a floating-point number 
        # representing the number of seconds since the epoch (January 1, 1970)
        # when the file was last modified."
        # then compare the two time
        # if the time from the request >= file last modified time, then return 304

        # case 5: 200 OK

        #connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()


while True:
    connectionSocket, addr = serverSocket.accept()

    # client acquire the lock
    thread_lock.acquire()
    print('address:', addr[0], ':', addr[1])

    # open a new thread
    start_new_thread(mutil_thread,(connectionSocket,))
    # connectionSocket.close()

serverSocket.close()