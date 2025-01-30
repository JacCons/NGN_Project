import socket
import sys

Error = "Specify the Server's IP"
if (sys.argv[1] == ''):
    exit (Error)

HOST = str(sys.argv[1]) # Server IP address

PORT = 12345  # Service port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    data = client_socket.recv(1024) # Receive up to 1024 bytes
    print(f"{data.decode()}")