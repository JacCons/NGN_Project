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
import socket
import json

Directories = {
    'serv1': './Servers/server1.txt',
    'serv2': './Servers/server2.txt',
    'serv3': './Servers/server3.txt',
    'serv4': './Servers/server4.txt',
    'serv1_path': './Servers/server1_path.txt',
    'serv2_path': './Servers/server2_path.txt',
    'serv3_path': './Servers/server3_path.txt',
    'serv4_path': './Servers/server4_path.txt'
}


shortest_path_date =[]




# Imposta il backend di matplotlib su Agg
plt.switch_backend('Agg')

# Creazione del grafo
G = nx.Graph()
default_client = '10.0.0.1'

class MyTopo (Topo):    
    def build(self):

        try:
            with open("topology_parameters.txt", "r") as f:
                valori = f.readlines()
                n_host = int(valori[0].strip())
                n_switch = int(valori[1].strip())
        except FileNotFoundError:
            print("Errore: Il file non esiste")
        except (IndexError, ValueError):
            print("Errore: il file contiene dati non validi")
        
        hosts_NODES=[]
        hosts_MN=[] #array of hosts
        switch_NODES=[]
        switch_MN=[] #array of switches
        link_NODES = []

        # Adding hosts
        for i in range (n_host):
            hostname = f"h{i+1}"
            hosts_NODES.append(hostname)
            hosts_MN.append(self.addHost(hostname))
        G.add_nodes_from(hosts_NODES, type="host")
       
        #Print all hosts
        print ("----Hosts----")
        print (hosts_NODES)
        print("\n")

        for k in range (n_switch):
            switchname = f"s{k+1}"
            switch_NODES.append(switchname)
            switch_MN.append(self.addSwitch(switchname,protocols='OpenFlow13',stp = True))
        G.add_nodes_from(switch_NODES, type="switch")
        
        #Print all switches
        print ("----Switches----")
        print (switch_NODES)
        print("\n")

        # Assign hosts to switches
        for host in hosts_NODES:
            switch = random.choice(switch_NODES)
            self.addLink(host, switch) #add link host-switch
            link_NODES.append (f"({host},{switch})") #to print when starting the mininet
            G.add_edge(host, switch)
        
        random.shuffle(switch_NODES)
        for i in range (n_switch-1):
            switch1 = switch_NODES[i]
            switch2 = switch_NODES[i+1]
            self.addLink(switch1, switch2)
            link_NODES.append (f"({switch1},{switch2})") #to print when starting the mininet
            G.add_edge(switch1, switch2)
        
        temp = []
        #for cycle from 0 to the second-to-last switch (doesn't work)
        for i in range (n_switch-2):
            #clear the temporary array
            temp.clear()
            #assign to switch 1 the selected switch in switch_NODES
            switch1 = switch_NODES[i]
            #random number of non adjacent (+2) links a switch can have
            n_links= random.randint(0,n_switch-(i+2)) 
            
            #fill the temporary array
            temp = switch_NODES[i + 2:]
            
            #create the new links (doesn't work properly with mininet)
            for _ in range (n_links):
                #select a random switch in the temp list
                if not temp:  # Stop if no more candidates
                    break
                switch2 = random.choice(temp)
                #remove the selected switch from the temp list to avoid having duplicate links
                temp.remove(switch2)
                if not G.has_edge(switch1, switch2):
                    self.addLink(switch1, switch2)
                    link_NODES.append (f"({switch1},{switch2})") #to print when starting the mininet
                    G.add_edge(switch1, switch2)
        
        #Print links
        print ("----Links----")
        print(link_NODES)
        print("\n")
            
        # Create graph
        pos = nx.spring_layout(G, k=3.5 , iterations=500)  # Layout per una visualizzazione più chiara con seme fisso
        colors = ["#c679d9" if G.nodes[node]['type'] == "host" else "#64c1d1" for node in G.nodes]
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, font_size=10)
        plt.savefig("img/graph.png")
        print("Graph saved as graph.png\n")
        plt.clf()  # Pulisce la figura corrente
    
    def print_shortest_path_to_GUI(net, dst_host):
        shortest_path = MyTopo.get_shortest_path(net, default_client , dst_host)
        print(f"\nShortest path between client and server: {shortest_path}")
        

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
        # switch_connections = {}
        # for switch in net.switches:
        #     switch_connections[switch.name] = {}
        #     for link in net.links:
        #         if link.intf1.node.name == switch.name:
        #             neighbor_switch = link.intf2.node.name
        #         elif link.intf2.node.name == switch.name:
        #             neighbor_switch = link.intf1.node.name
        #         else:
        #             continue
        #         # Assign a random weight to each link
        #         weight = random.randint(1, 10)
        #         switch_connections[switch.name][neighbor_switch] = weight
        #         G.add_edge(switch.name, neighbor_switch, weight=weight)  # Aggiorna il grafo G con il peso
        
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
        # Calculate shortest path using Dijkstra's algorithm and weights
        # shortest_path = nx.shortest_path(G, source=src_switch, target=dst_switch, weight='weight')

        # Draw the graph with weights

        # Usa lo stesso seme per una disposizione coerente
        # Aumenta il valore di k per più spazio
        # pos = nx.spring_layout(G, k=3)   
        # edge_labels = nx.get_edge_attributes(G, 'weight')
        # node_colors = ["red" if G.nodes[node].get('type') == "host" else "blue" for node in G.nodes]
        # nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=11)
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        # plt.savefig("img/graph_with_weights.png")
        # print("\nGraph with weights saved as graph_with_weights.png")
        # plt.close()  # Chiude la figura corrente

        return shortest_path
    
#FUNCTIONS
def wait_for_stp_convergence(timeout=30):
    """Waiting for STP to converge."""
    print(f"Waiting for STP to converge ({timeout} seconds)...")
    time.sleep(timeout)
    print("STP convergence achieved...")

def assign_services():
    """Controlla il file per avviare o fermare il servizio."""
    service_started1 = False 
    service_started2 = False 
    service_started3 = False
    service_started4 = False
    
    host_server1 = net.get('h3')
    host_server2 = net.get('h4')
    host_server3 = net.get('h6')
    host_server4 = net.get('h7')

    while True:
        try:
            with open(Directories["serv1"], "r") as file:
                stato = file.read().strip()  # Leggi il contenuto del file
                if stato == "on" and not service_started1 :
                    print(f"\nStarting Server 1 on host {host_server1}...")
                    print(f"Server IP: {host_server1.IP()}")
                    host_server1.cmd('python3 ./Servers/server1.py &')  # Avvia il server in background 
                    time.sleep(3)
                    print(f"Server 1 running...")  # Avvia il server in background
                    print("press Enter to continue...")
                    service_started1 = True
                elif stato == "off" and service_started1:
                    print("Server1 stopped!")
                    host_server1.cmd('pkill -f ./Servers/server1.py &')  # Ferma il server
                    print("press Enter to continue...")
                    service_started1 = False
        except Exception as e:
            print(f"Errore nel monitoraggio del file: {e}")
        time.sleep(1)  # Controlla ogni secondo
        

        try:
            with open(Directories["serv2"], "r") as file:
                stato = file.read().strip()  # Leggi il contenuto del file
                if stato == "on" and not service_started2 :
                    print(f"\nStarting Server 2 on host {host_server2}...")
                    print(f"Server IP: {host_server2.IP()}")
                    host_server2.cmd('python3 ./Servers/server2.py &')  # Avvia il server in background 
                    time.sleep(3)
                    print(f"Server 2 running...")  # Avvia il server in background
                    print("press Enter to continue...")
                    service_started2 = True
                elif stato == "off" and service_started2:
                    print("Server2 stopped!")
                    host_server1.cmd('pkill -f ./Servers/server2.py &')  # Ferma il server
                    print("press Enter to continue...")
                    service_started2 = False
        except Exception as e:
            print(f"Errore nel monitoraggio del file: {e}")
        time.sleep(1)  # Controlla ogni secondo


        try:
            with open(Directories["serv3"], "r") as file:
                stato = file.read().strip()  # Leggi il contenuto del file
                if stato == "on" and not service_started3 :
                    print(f"\nStarting Server 3 on host {host_server3}...")
                    print(f"Server IP: {host_server3.IP()}")
                    host_server3.cmd('python3 ./Servers/server3.py &')  # Avvia il server in background 
                    time.sleep(3)
                    print(f"Server 3 running...")  # Avvia il server in background
                    print("press Enter to continue...")
                    service_started3 = True
                elif stato == "off" and service_started3:
                    print("Server3 stopped!")
                    host_server3.cmd('pkill -f ./Servers/server3.py &')  # Ferma il server
                    print("press Enter to continue...")
                    service_started3 = False
        except Exception as e:
            print(f"Errore nel monitoraggio del file: {e}")
        time.sleep(1)  # Controlla ogni secondo


        try:
            with open(Directories["serv4"], "r") as file:
                stato = file.read().strip()  # Leggi il contenuto del file
                if stato == "on" and not service_started4 :
                    print(f"\nStarting Server 4 on host {host_server4}...")
                    print(f"Server IP: {host_server4.IP()}")
                    host_server4.cmd('python3 ./Servers/server4.py &')  # Avvia il server in background 
                    time.sleep(3)
                    print(f"Server 4 running...")  # Avvia il server in background
                    print("press Enter to continue...")
                    service_started4 = True
                elif stato == "off" and service_started4:
                    print("Server4 stopped!")
                    host_server4.cmd('pkill -f ./Servers/server4.py &')  # Ferma il server
                    print("press Enter to continue...")
                    service_started4 = False
        except Exception as e:
            print(f"Errore nel monitoraggio del file: {e}")
        time.sleep(1)  # Controlla ogni secondo

def write_csv_net():
    with open("net.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        # Scrivi l'intestazione del CSV
        writer.writerow(["Source", "SrcPort", "Dest.", "DstPort"])
        
        for node in net.values():
            for intf in node.intfList():
                if intf.link:  # Controlla se c'è un link associato
                    # Ottieni il peer e la sua interfaccia
                    peer_intf = intf.link.intf2 if intf.link.intf1 == intf else intf.link.intf1
                    intf_name = intf.name.split('-')[-1]
                    peer_intf_name = peer_intf.name.split('-')[-1]
                    writer.writerow([node.name, intf_name, peer_intf.node.name, peer_intf_name])

# def send_socket_data():
#     # Set up the client
#     HOST = '127.0.0.1'  # Server's IP address
#     PORT = 10000       # Server's port

#     variable_to_send = "Hello, Server!"  # Variable to send

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#         client_socket.connect((HOST, PORT))
#         # Send data
        
#         data_to_send = json.dumps(shortest_path_date).encode('utf-8')
#         client_socket.sendall(data_to_send)
#         print(f"Sent variable: {shortest_path_date}")

def write_csv_path(shortest_path_date, file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Scrivi l'intestazione del CSV
        writer.writerow(["Source", "Dest."])
        
        for i in range(len(shortest_path_date) - 1):
            writer.writerow([shortest_path_date[i], shortest_path_date[i+1]])


def run_minimal_network():
    
    # Connect Mininet to the already running Ryu controller at localhost:6653
    c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
    
    # Create the network using the custom topology and connect it to the Ryu controller
    global net
    net = Mininet(topo=MyTopo(), switch=OVSSwitch, controller=c0, autoSetMacs=True)

    # Start the network
    net.start()

    #wait_for_stp_convergence(timeout=3)
    
    write_csv_net()

    client = net.get('h1')
    server1 = net.get('h3')
    shortest_path_date = MyTopo.get_shortest_path(net, client, server1)
    print(f"\nShortest path between h1 and h2: {shortest_path_date}\n")

    write_csv_path(shortest_path_date, Directories["serv1_path"])



    # send_socket_data()

    # # Check if hosts were found before proceeding
    # if h1 is None or h2 is None:
    #     print("Error: Hosts h1 or h2 not found in the network.")
    #     net.stop()
    #     return

    # (Optional) Verify connectivity between hosts
    #print("Testing connectivity...")
    #net.pingAll()

    # Now that h1 and h2 are guaranteed to be valid objects, call get_shortest_path
 

    # Start the CLI for manual interaction

    # Avvia il monitoraggio del file in un thread separato
    monitor_thread = threading.Thread(target=assign_services)
    monitor_thread.daemon = True  # Questo farà terminare il thread quando il programma principale termina
    monitor_thread.start()

    CLI(net)

    # Stop the network when exiting the CLI
    net.stop()



if __name__ == '__main__': 
    run_minimal_network()


