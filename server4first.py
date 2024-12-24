import socket

HOST = ''  # Ascolta su tutte le interfacce
PORT = 12345  # Porta di ascolto

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server in ascolto sulla porta {PORT}...")

    HOST_FORWARD = "10.0.0.3"  # Indirizzo IP del server h3
    PORT_FORWARD= 12345 # Porta del servizio

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST_FORWARD, PORT_FORWARD))
        data = client_socket.recv(1024)  # Riceve fino a 1024 byte


    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connessione da {addr}")
            conn.sendall(data.encode())  


