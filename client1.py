import socket

#tradurre nome host con IP
HOST = '10.0.0.1'  # Indirizzo IP dell'host 1
PORT = 12345       # Porta del servizio

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    data = client_socket.recv(1024)  # Riceve fino a 1024 byte
    print(f"Data e ora ricevute: {data.decode()}")