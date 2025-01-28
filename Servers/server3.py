import socket
import random

HOST = ''  # Ascolta su tutte le interfacce
PORT = 12345  # Porta di ascolto

famous_quotes = [
    "To be, or not to be, that is the question. - William Shakespeare",
    "The only thing we have to fear is fear itself. - Franklin D. Roosevelt",
    "It is never too late to be what you might have been. - George Eliot",
    "In three words I can sum up everything I've learned about life: it goes on. - Robert Frost",
    "All that is gold does not glitter, not all those who wander are lost. - J.R.R. Tolkien",
    "A room without books is like a body without a soul. - Marcus Tullius Cicero",
    "Do I dare disturb the universe? - T.S. Eliot",
    "Not all those who wander are lost. - J.R.R. Tolkien",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "The truth will set you free, but first it will make you miserable. - James A. Garfield"
]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on port {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connection from {addr}")
            random_quote = random.choice(famous_quotes)
            random_quote = "Daily quote: "+ random_quote
            conn.sendall(random_quote.encode())  
