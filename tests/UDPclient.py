from socket import *

hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverName = IPAddr
serverPort = 1200

clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(),(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print('what a great upcase sentence:', modifiedMessage.decode())
clientSocket.close()