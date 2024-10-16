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

        # message = message.decode()
        print(message)

        capitalizedSentence = message.upper()
        connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()


while True:
    connectionSocket, addr = serverSocket.accept()
    
    # sentence = connectionSocket.recv(1024).decode()
    # capitalizedSentence = sentence.upper()
    # connectionSocket.send(capitalizedSentence.encode())

    # client acquire the lock
    thread_lock.acquire()
    print('address:', addr[0], ':', addr[1])

    # open a new thread
    start_new_thread(mutil_thread,(connectionSocket,))
    # connectionSocket.close()

serverSocket.close()