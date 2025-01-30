import socket
from datetime import datetime

# Configurazione
LISTEN_HOST = '' # Listen on all interfaces
LISTEN_PORT = 12345  # Listening port
REMOTE_HOST = '10.0.0.3'  # Remote server address
REMOTE_PORT = 12345 # Remote server port

# 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: #creates a socket 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #if the port is in use, it will be reused
    server_socket.bind((LISTEN_HOST, LISTEN_PORT))
    server_socket.listen() #listen for incoming connections
    print(f"Server listening on port {LISTEN_PORT}...")

    while True:
        conn, addr = server_socket.accept() #accepts incoming connection
        with conn:
            print(f"Connection from {addr}")

            #Create a new socket for the remote server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
                remote_socket.connect((REMOTE_HOST, REMOTE_PORT))
                remote_socket.sendall(b"Request for data") #Send request to the remote server
                data = remote_socket.recv(1024)  #Receive data from the remote server

                #Modify the data and send it to the local client
                if data:
                    data = data.decode() + ", Time: " + datetime.now().time().strftime("%H:%M:%S") + " GMT"
                    conn.sendall(data.encode())
            




