import socket
import random

HOST = ''  # Ascolta su tutte le interfacce
PORT = 12345  # Porta di ascolto

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server in ascolto sulla porta {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connessione da {addr}")
            number = random(100)
            conn.sendall(number.encode())  
