# Step Two: Build Your Minimal Web Server & Test

a)  The combination of HTTPfunctions.py and TCPServer.py make up our server
    Our server can only respond to GET requests, all other requests will be answered
    as 501 Not Implement. 

b)  Using the link in a web browers works, while the server is running of course.

c)  It the provided servertests.sh are curl commands that test our server functionallity
    you can run the test on lunix by running the command:
    bash servertests.sh [IP_address_of_server] [Port] [url]
    the bash scripts output into files needed for the functionallity they test. 
    We have submited what those file when we ran the script.