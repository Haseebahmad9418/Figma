import socket
import time


serverAddressPort = ("127.0.0.1", 20002)

bufferSize = 1024

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
while True:
    # msgFromClient = "Hello UDP Server"
    msgFromClient = "101,48.7758° N, 9.1829° E,Stuttgart"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "102,okay"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "103,ohh"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "104,ohh"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "105,okay"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "106,44"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "201,conct"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "202,['sam','iphone','dgfs','sdfs','adfas','sdferg']"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "203,44"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "204,conct"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "205,244"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromClient = "206,44"
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)