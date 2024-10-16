from socket import *

hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverName = IPAddr
serverPort = 1200

clientSocket = socket(AF_INET, SOCK_DGRAM)
message = ('Input lowercase sentence: what a great upcase sentence')
clientSocket.sendto(message.encode(),(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()