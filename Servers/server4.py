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
            data = data.decode()  # Decodifica i dati ricevuti dal server remoto
            data = data + " altro server !"
            conn.sendall(data.encode())  # Invia i dati ricevuti dal server remoto



