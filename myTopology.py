import networkx as nx
import matplotlib.pyplot as plt
import random
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController
import time
import threading
import csv


Directories = {
    'serv1': './Servers/server1.txt',
    'serv2': './Servers/server2.txt',
    'serv3': './Servers/server3.txt',
    'serv4': './Servers/server4.txt',
    'serv1_path': './Servers/server1_path.csv',
    'serv2_path': './Servers/server2_path.csv',
    'serv3_path': './Servers/server3_path.csv',
    'serv4_path': './Servers/server4_path.csv'
}

class MyTopo(Topo):
    "Rete minima con due switch e due host."

    def build(self):  
        # Aggiungi host
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
     
        # Aggiungi switch
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', protocols='OpenFlow13')
        s4 = self.addSwitch('s4', protocols='OpenFlow13')
        
        # Aggiungi i link
        self.addLink(h1, s1, intfName2=f'{s1}-eth1')
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s2, s4)

        
shortest_path_date =[]

def get_shortest_path(src_host, dst_host):
    src_switch = src_host.defaultIntf().node.name  # Access switch through default interface
    dst_switch = dst_host.defaultIntf().node.name  # Access switch through default interface
    shortest_path = nx.shortest_path(G, source=src_switch, target=dst_switch)
    print(f"\nShortest path between client and server without weights: {shortest_path}")
    return shortest_path


def wait_for_stp_convergence(timeout=30):
    """Aspetta che STP converga."""
    print(f"Attesa per la convergenza di STP (fino a {timeout} secondi)...")
    time.sleep(timeout)
    print("Convergenza STP completata o timeout raggiunto.")


def monitor_file_for_service(h1):
    """Controlla il file per avviare o fermare il servizio."""
    service_started = False
    while True:
        try:
            with open("server1.txt", "r") as file:
                stato = file.read().strip()  # Leggi il contenuto del file
                if stato == "on" and not service_started :
                    print("Servizio avviato su h1!")
                    h1.cmd('nohup python3 server1.py > /dev/null 2>&1 & ')  # Avvia il server in background
                    print("press Enter to continue...")
                    time.sleep(3)  # Attendi che il server sia pronto
                    service_started = True
                elif stato == "off" and service_started:
                    print("Servizio fermato su h1!")
                    h1.cmd('nohup pkill -f server1.py > /dev/null 2>&1 &')  # Ferma il server
                    print("press Enter to continue...")
                    service_started = False
                    
        except Exception as e:
            print(f"Errore nel monitoraggio del file: {e}")
        time.sleep(1)  # Controlla ogni secondo

def write_csv_path(shortest_path_date, file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Scrivi l'intestazione del CSV
        writer.writerow(["Source","Dest."])
        
        for i in range(1, len(shortest_path_date) - 1):
            writer.writerow([shortest_path_date[i], shortest_path_date[i+1]])

# def write_csv_net_a():
#     with open("net.csv", mode='w', newline='') as file:
#         writer = csv.writer(file)
#         # Scrivi l'intestazione del CSV
#         writer.writerow(["Source", "SrcPort", "Dest.", "DstPort", "SrcMAC", "DstMAC"])

#         # Itera attraverso tutti i nodi (switch e host)
#         for node in net.values():
#             for intf in node.intfList():
#                 if intf.link:  # Controlla se c'è un link associato
#                     # Ottieni il peer e la sua interfaccia
#                     peer_intf = intf.link.intf2 if intf.link.intf1 == intf else intf.link.intf1
#                     intf_name = intf.name.split('-')[-1]  # Nome della porta della sorgente
#                     peer_intf_name = peer_intf.name.split('-')[-1]  # Nome della porta di destinazione
                    
#                     # Ottieni il MAC address per le interfacce
#                     src_mac = intf.MAC()  # MAC address per l'interfaccia sorgente
#                     dst_mac = peer_intf.MAC()  # MAC address per l'interfaccia di destinazione
                    
#                     # Scrivi la riga nel file CSV
#                     writer.writerow([node.name, intf_name, peer_intf.node.name, peer_intf_name, src_mac, dst_mac])


def run_minimal_network():
    # Connetti Mininet al controller Ryu su localhost:6653
    c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
    
    # Crea la rete con la topologia personalizzata e il controller Ryu
    global net
    net = Mininet(topo=MyTopo(), switch=OVSSwitch, controller=c0, autoSetMacs=True)
    
    # Avvia la rete
    net.start()
    net.staticArp()
    print("Rete avviata.")
    
    #Attendi la convergenza di STP
    #wait_for_stp_convergence(timeout=3)

    # write_csv_net_a()
    
    client = net.get('h1')
    server1 = net.get('h3')
    shortest_path_date = ['h1','s1','s2','s3','h3']
    print(f"\nShortest path between h1 and h3: {shortest_path_date}\n")

    # Verifica connessione con ping
    # print("Testing connectivity between hosts...")
    # if net.ping([h1, h2]) > 0:
    #     print("Ping failed after STP convergence. Exiting.")
    #     net.stop()
    #     return


    write_csv_path(shortest_path_date, Directories["serv1_path"])


    # Ottieni la prima interfaccia dello switch (eth0, eth1, ecc.)
    #switch_intf = switch.  # Prima interfaccia (può essere eth0, eth1, ecc.)

    # Ottieni il MAC address dell'interfaccia
    #mac_address = switch_intf.MAC()

    # Avvia il monitoraggio del file in un thread separato
    # monitor_thread = threading.Thread(target=monitor_file_for_service, args=(h1,))
    # monitor_thread.daemon = True  # Questo farà terminare il thread quando il programma principale termina
    # monitor_thread.start()

    # Avvia il client su h2
    # print("Avvio del client su h2...")
    # result_client = h2.cmd(f'python3 client1.py {h1.IP()}')
    # print(f"Client output:\n{result_client}")
    
    # Avvia la CLI per interazione manuale
    CLI(net)
    
    # Ferma la rete quando esci dalla CLI
    net.stop()
    # try:
    #     with open("server1.txt", "r") as file:
    #         file.write('off')                  
    # except Exception as e:
    #     print(f"Errore nel monitoraggio del file: {e}")
    #     time.sleep(1)  # Controlla ogni sec


if __name__ == '__main__':
    run_minimal_network()

