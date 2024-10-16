from socket import *

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

serverName = IPAddr
serverPort = 1200