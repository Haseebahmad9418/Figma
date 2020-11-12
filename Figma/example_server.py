from socket import socket, AF_INET, SOCK_DGRAM
localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
# Create a datagram socket
UDPServerSocket = socket(family=AF_INET, type=SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
# Listen for incoming datagrams
while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    if message == b's':
        msgFromServer = "s,Success"
        print(msgFromServer)
        bytesToSend = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address)
    elif message == b'0':
        msgFromServer = "0,Success"
        print(msgFromServer)
        bytesToSend = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address)
    elif message == b'c':
        pass
    else:
        print("Nothing")
        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)