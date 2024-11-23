import socket
import sys
from mininet.net import Mininet
#run this command: h(x) python3 client1.py 
#tradurre nome host con IP
#host_name = sys.argv
#host_ = net.get(hostname)
#host_ip = host_.IP()

Error = "Specify the Server's IP"
if (sys.argv[1] == ''):
    exit (Error)

HOST = str(sys.argv[1])  # Indirizzo IP del server

PORT = 12345       # Porta del servizio

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    data = client_socket.recv(1024)  # Riceve fino a 1024 byte
    print(f"Data e ora ricevute: {data.decode()}")

    #trovare un modo per differenziare il servizio del server