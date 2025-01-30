import socket
import random

HOST = ''  # Listen on all interfaces
PORT = 12345  # Listening port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on port {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connection from {addr}")
            number = "Lucky number: " + str(random.randint(0, 99))
            conn.sendall(number.encode())  
