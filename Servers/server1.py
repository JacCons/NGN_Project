import socket
from datetime import datetime

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
            now = "Date and Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.sendall(now.encode())  # Invia la data e ora
