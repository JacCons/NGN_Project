import socket
from datetime import datetime

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
            now = "Date and Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.sendall(now.encode())  # Invia la data e ora
