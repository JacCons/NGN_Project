import networkx as nx
import matplotlib.pyplot as plt
import random
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController
import time


# Imposta il backend di matplotlib su Agg
plt.switch_backend('Agg')

#ssh -X -p 2222 vagrant@localhost

# Creazione del grafo
G = nx.Graph()

class MyTopo (Topo):    
    def build(self):
        
        n_host = 8
        n_switch = 7
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
        pos = nx.spring_layout(G, seed=42)  # Layout per una visualizzazione più chiara con seme fisso
        colors = ["red" if G.nodes[node]['type'] == "host" else "blue" for node in G.nodes]
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, font_size=10)
        plt.savefig("img/graph.png")
        print("Graph saved as graph.png\n")
        plt.clf()  # Pulisce la figura corrente
        

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
                weight = random.randint(1, 10)
                switch_connections[switch.name][neighbor_switch] = weight
                G.add_edge(switch.name, neighbor_switch, weight=weight)  # Aggiorna il grafo G con il peso
        
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
        print(f"\nShortest path between h1 and h2 without weights: {shortest_path}")
        # Calculate shortest path using Dijkstra's algorithm and weights
        shortest_path = nx.shortest_path(G, source=src_switch, target=dst_switch, weight='weight')

        # Draw the graph with weights

        # Usa lo stesso seme per una disposizione coerente
        # Aumenta il valore di k per più spazio
        pos = nx.spring_layout(G, k=3)   
        edge_labels = nx.get_edge_attributes(G, 'weight')
        node_colors = ["red" if G.nodes[node].get('type') == "host" else "blue" for node in G.nodes]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=11)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.savefig("img/graph_with_weights.png")
        print("\nGraph with weights saved as graph_with_weights.png")
        plt.close()  # Chiude la figura corrente

        return shortest_path
    
#FUNCTIONS
def wait_for_stp_convergence(timeout=30):
    """Waiting for STP to converge."""
    print(f"Waiting for STP to converge ({timeout} seconds)...")
    time.sleep(timeout)
    print("STP convergence achieved...")

def assign_services(net):
    #Host client sarà poi rimosso perché i servizi saranno on demand
    host_client = net.get('h1')
    host_server1 = net.get('h3')
    #host_server2 = net.get('h4')
    #host_server3 = net.get('h6')
    host_server4 = net.get('h7')
    
    # Attendi la convergenza di STP
    wait_for_stp_convergence(timeout=30)
    
    
    print("Testing connectivity between hosts...")
    if net.ping([host_server1,host_client ]) > 0:
        print("Ping failed after STP convergence. Exiting.")
        net.stop()
        return

    # Avvia il server su h1
    print(f"\nStarting Server 1 on host {host_server1}...")
    #server_ip = host_server1.IP()  # Ottieni l'indirizzo IP dinamico di h1
    print(f"Server IP: {host_server1.IP()}")
    host_server1.cmd('python3 server1.py &')  # Avvia il server in background 
    # Waiting for the server to be ready
    time.sleep(3)
    print(f"Server 1 running...")

    # Avvia il server su h7
    print(f"\nStarting Server 4 on host {host_server4}...")
    #server_ip = host_server1.IP()  # Ottieni l'indirizzo IP dinamico di h1
    print(f"Server IP: {host_server4.IP()}")
    host_server4.cmd('python3 server4first.py &')  # Avvia il server in background 
    # Waiting for the server to be ready
    time.sleep(3)
    print(f"Server 4 running...")

    # Avvia il client su h2 (da rimuovere successivamente!!!!!)
    print("\nAvvio del client su h1...")
    result_client = host_client.cmd(f'python3 client4.py {host_server4.IP()}')
    print(f"Client output:\n{result_client}")


def run_minimal_network():
    
    # Connect Mininet to the already running Ryu controller at localhost:6653
    c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
    
    # Create the network using the custom topology and connect it to the Ryu controller
    net = Mininet(topo=MyTopo(), switch=OVSSwitch, controller=c0)

    # Start the network
    net.start()
    assign_services(net)
    

    # # Check if hosts were found before proceeding
    # if h1 is None or h2 is None:
    #     print("Error: Hosts h1 or h2 not found in the network.")
    #     net.stop()
    #     return

    # (Optional) Verify connectivity between hosts
    #print("Testing connectivity...")
    #net.pingAll()

    # Now that h1 and h2 are guaranteed to be valid objects, call get_shortest_path
    #shortest_path = MyTopo.get_shortest_path(net, h1, h2)
    #print(f"\nShortest path between h1 and h2: {shortest_path}\n")

    # Start the CLI for manual interaction
    CLI(net)

    

    # Stop the network when exiting the CLI
    net.stop()

if __name__ == '__main__': 
    run_minimal_network()


