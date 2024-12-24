from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
import time

class MyTopo(Topo):
    "Rete minima con due switch e due host."

    def build(self):  
        # Aggiungi host
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
     
        # Aggiungi switch
        s1 = self.addSwitch('s1', protocols='OpenFlow13', stp=True)
        s2 = self.addSwitch('s2', protocols='OpenFlow13', stp=True)
        s3 = self.addSwitch('s3', protocols='OpenFlow13', stp=True)
        s4 = self.addSwitch('s4', protocols='OpenFlow13', stp=True)
        
        # Aggiungi i link
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s4, s1)


def wait_for_stp_convergence(timeout=30):
    """Aspetta che STP converga."""
    print(f"Attesa per la convergenza di STP (fino a {timeout} secondi)...")
    time.sleep(timeout)
    print("Convergenza STP completata o timeout raggiunto.")


def run_minimal_network():
    # Connetti Mininet al controller Ryu su localhost:6653
    c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
    
    # Crea la rete con la topologia personalizzata e il controller Ryu
    net = Mininet(topo=MyTopo(), switch=OVSSwitch, controller=c0)
    
    # Avvia la rete
    net.start()
    print("Rete avviata.")
    
    # Attendi la convergenza di STP
    wait_for_stp_convergence(timeout=30)

    # Recupera gli host dalla rete
    h1 = net.get('h1')  # Ottieni oggetto host h1
    h2 = net.get('h2')  # Ottieni oggetto host h2

    # Verifica connessione con ping
    print("Testing connectivity between hosts...")
    if net.ping([h1, h2]) > 0:
        print("Ping failed after STP convergence. Exiting.")
        net.stop()
        return

    # Avvia il server su h1
    print("Avvio del server su h1...")
    server_ip = h1.IP()  # Ottieni l'indirizzo IP dinamico di h1
    print(f"Server IP: {server_ip}")
    h1.cmd('python3 server1.py &')  # Avvia il server in background
    print(f"Server avviato...")
    
    # Attendi che il server sia pronto
    time.sleep(3)

    # Avvia il client su h2
    print("Avvio del client su h2...")
    result_client = h2.cmd(f'python3 client1.py {server_ip}')
    print(f"Client output:\n{result_client}")
    
    # Avvia la CLI per interazione manuale
    CLI(net)
    
    # Ferma la rete quando esci dalla CLI
    net.stop()

if __name__ == '__main__':
    run_minimal_network()
