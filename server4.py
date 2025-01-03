# import socket

# HOST = ''  # Ascolta su tutte le interfacce
# PORT = 12345  # Porta di ascolto

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

#     HOST_FORWARD = '10.0.0.3'  # Indirizzo IP del server h3
#     PORT_FORWARD= 12345 # Porta del servizio

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#         client_socket.connect((HOST_FORWARD, PORT_FORWARD))
#         data = client_socket.recv(1024)  # Riceve fino a 1024 byte

#     server_socket.bind((HOST, PORT))
#     server_socket.listen()
#     print(f"Server in ascolto sulla porta {PORT}...")

#     while True:
#         conn, addr = server_socket.accept()
#         with conn:
#             print(f"Connessione da {addr}")
#             conn.sendall(data.encode())  

import socket

# Configurazione
LISTEN_HOST = ''  # Ascolta su tutte le interfacce
LISTEN_PORT = 12345  # Porta per i client locali

REMOTE_HOST = '10.0.0.3'  # Indirizzo del server remoto
REMOTE_PORT = 12345       # Porta del server remoto

# Connessione al server remoto
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
    remote_socket.connect((REMOTE_HOST, REMOTE_PORT))
    data = remote_socket.recv(1024)  # Riceve dati dal server remoto

# Server per inoltrare i dati ai client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((LISTEN_HOST, LISTEN_PORT))
    server_socket.listen()
    print(f"Server in ascolto sulla porta {LISTEN_PORT}...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connessione da {addr}")
            conn.sendall(data)  # Invia i dati ricevuti dal server remoto



