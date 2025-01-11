import time
import threading
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
import networkx as nx
import random
from simple_switch_stp_13 import SimpleSwitch13
import ryu.lib.stplib as stplib

G = nx.Graph()

class MyTopo(Topo):
    "Rete minima con due switch e due host."

    def build(self):  
        # Aggiungi host
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        G.add_nodes_from(h1, type="host")
        G.add_nodes_from(h2, type="host")
        G.add_nodes_from(h3, type="host")
        G.add_nodes_from(h4, type="host")

     
        # Aggiungi switch
        s1 = self.addSwitch('s1', protocols='OpenFlow13', stp=True)
        s2 = self.addSwitch('s2', protocols='OpenFlow13', stp=True)
        s3 = self.addSwitch('s3', protocols='OpenFlow13', stp=True)
        s4 = self.addSwitch('s4', protocols='OpenFlow13', stp=True)

        G.add_nodes_from(s1, type="switch")
        G.add_nodes_from(s2, type="switch")
        G.add_nodes_from(s3, type="switch")
        G.add_nodes_from(s4, type="switch")

        
        # Aggiungi i link
        self.addLink(h1, s1)
        G.add_edge(h1, s1)  # Aggiorna il grafo G con il peso
        self.addLink(h2, s2)
        G.add_edge(h2, s2)
        self.addLink(h3, s3)
        G.add_edge(h3, s3)
        self.addLink(h4, s4)
        G.add_edge(h4, s4)


        self.addLink(s1, s2)
        G.add_edge(s1, s2)
        self.addLink(s2, s3)
        G.add_edge(s2, s3)
        self.addLink(s3, s4)
        G.add_edge(s3, s4)
        self.addLink(s4, s1)
        G.add_edge(s4, s1)

# def wait_for_stp_convergence(timeout=30):
#     """Aspetta che STP converga."""
#     print(f"Attesa per la convergenza di STP (fino a {timeout} secondi)...")
#     time.sleep(timeout)
#     print("Convergenza STP completata o timeout raggiunto.")


# def monitor_file_for_service(h1):
#     """Controlla il file per avviare o fermare il servizio."""
#     service_started = False
#     while True:
#         try:
#             with open("server1.txt", "r") as file:
#                 stato = file.read().strip()  # Leggi il contenuto del file
#                 if stato == "on" and not service_started :
#                     print("Servizio avviato su h1!")
#                     h1.cmd('nohup python3 server1.py > /dev/null 2>&1 & ')  # Avvia il server in background
#                     print("press Enter to continue...")
#                     time.sleep(3)  # Attendi che il server sia pronto
#                     service_started = True
#                 elif stato == "off" and service_started:
#                     print("Servizio fermato su h1!")
#                     h1.cmd('nohup pkill -f server1.py > /dev/null 2>&1 &')  # Ferma il server
#                     print("press Enter to continue...")
#                     service_started = False
                    
#         except Exception as e:
#             print(f"Errore nel monitoraggio del file: {e}")
#         time.sleep(1)  # Controlla ogni secondo


def get_shortest_path(net, src_host, dst_host):
    """
    Calculates the shortest path between two hosts in the Mininet network.

    Args:
        net: The Mininet network object.
        src_host: The source host object.
        dst_host: The destination host object.

    Returns:
        A list of switches representing the shortest path between the hosts.
    """
    # Get switch connections from Mininet network
    switch_connections = {}
    for switch in net.switches:
        switch_connections[switch.name] = {}
        for link in net.links:
            if link.intf1.node.name == switch.name:
                neighbor_switch = link.intf2.node.name
            elif link.intf2.node.name == switch.name:
                neighbor_switch = link.intf1.node.name
            else:
                continue
            # Assign a random weight to each link
    # Stampa i collegamenti e i loro pesi
    # for switch, connections in switch_connections.items():
    #     print(f"Switch {switch} connections:")
    #     for neighbor, weight in connections:
    #         print(f"  -> {neighbor} with weight {weight}")

    # Get source and destination switch names
    src_switch = src_host.defaultIntf().node.name  # Access switch through default interface
    dst_switch = dst_host.defaultIntf().node.name  # Access switch through default interface

    # Calculate shortest path using Dijkstra's algorithm
    shortest_path = nx.shortest_path(G, source=src_switch, target=dst_switch)
    print(f"\nShortest path between client and server without weights: {shortest_path}")

    return shortest_path

def run_minimal_network():
    # Connetti Mininet al controller Ryu su localhost:6653
    c0 = RemoteController('c0', ip='127.0.0.1', port=6653)  # Usa RemoteController per Ryu
    
    # Crea la rete con la topologia personalizzata e il controller Ryu
    net = Mininet(topo=MyTopo(), switch=OVSSwitch, controller=c0)
    
    # Avvia la rete
    net.start()
    print("Rete avviata.")
    
    # Ottieni gli IP degli host
    h1 = net.get('h1')
    h1_ip = h1.IP()
    h3 = net.get('h3')
    h3_ip = h3.IP()

    path = get_shortest_path(net, h1, h3)

    # Accedi all'applicazione SimpleSwitch13 e installa il percorso
    app = c0#._controller  # Ottieni l'istanza dell'app Ryu dal controller Mininet
    if isinstance(app, SimpleSwitch13):
        app.install_path(path, h1_ip, h3_ip)  # Chiamato il metodo correttamente

    # Avvia la CLI per interazione manuale
    CLI(net)
    
    # Ferma la rete quando esci dalla CLI
    net.stop()



if __name__ == '__main__':
    run_minimal_network()


