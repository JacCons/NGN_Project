import networkx as nx
import matplotlib.pyplot as plt
import random
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController
import time
import threading


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


shortest_path_date =[]


# Set the matplotlib backend to Agg
plt.switch_backend('Agg')

# Create the graph
G = nx.Graph()

# Set the default client IP address
default_client = '10.0.0.1'

class MyTopo (Topo):    
    def build(self):
        
        # Read the number of hosts and switches from the file
        try:
            with open("./Tools/topology_parameters.txt", "r") as f:
                valori = f.readlines()
                n_host = int(valori[0].strip())
                n_switch = int(valori[1].strip())
        except FileNotFoundError:
            print("Errore: Il file non esiste")
        except (IndexError, ValueError):
            print("Errore: il file contiene dati non validi")
        
        hosts_NODES=[]
        hosts_MN=[] #array of hosts mininet objects
        switch_NODES=[]
        switch_MN=[] #array of switches mininet objects
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

        # Adding switches
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
            if(host == 'h1'):
                self.addLink(host, switch,intfName2=f'{switch}-eth1') #forzo lo switch 1 ad essere collegato ad eth1 dello switch
            else:
                self.addLink(host, switch)
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
        

    def get_shortest_path(src_host, dst_host):
        """
        Calculates the shortest path between two hosts in the Mininet network.

        Args:
            net: The Mininet network object.
            src_host: The source host object.
            dst_host: The destination host object.

        Returns:
            A list of switches representing the shortest path between the hosts.
        """
        #Get switch connections from Mininet network
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
                G.add_edge(switch.name, neighbor_switch, weight=weight) # Update graph G with weight
        
        #Print connections and their weights
        for switch, connections in switch_connections.items():
            print(f"Switch {switch} connections:")
            for neighbor, weight in connections:
                print(f"  -> {neighbor} with weight {weight}")

        # Get source and destination switch names
        src_switch = src_host.defaultIntf().node.name  # Access switch through default interface
        dst_switch = dst_host.defaultIntf().node.name  # Access switch through default interface

        # Calculate shortest path using Dijkstra's algorithm
        shortest_path = nx.shortest_path(G, source=src_switch, target=dst_switch)
        print(f"\nShortest path between client and server without weights: {shortest_path}")
        # Calculate shortest path using Dijkstra's algorithm and weights
        shortest_path = nx.shortest_path(G, source=src_switch, target=dst_switch, weight='weight')

        # Draw the graph with weights

        # Use the same seed for consistent layout
        # Increase k value for more space
        pos = nx.spring_layout(G, k=3)   
        edge_labels = nx.get_edge_attributes(G, 'weight')
        node_colors = ["red" if G.nodes[node].get('type') == "host" else "blue" for node in G.nodes]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=11)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.savefig("img/graph_with_weights.png")
        print("\nGraph with weights saved as graph_with_weights.png")
        plt.close()

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
    
    host_client = net.get('h1')
    host_server1 = net.get('h3')
    host_server2 = net.get('h4')
    host_server3 = net.get('h6')
    host_server4 = net.get('h7')

    while True:
        try:
            with open(Directories["serv1"], "r") as file:
                stato = file.read().strip()   #read the file
                if stato == "on" and not service_started1 :
                    print(f"\nStarting Server 1 IP: {host_server1.IP()} on host {host_server1} IP: {host_server1.IP()}...")
                    print(f"\n(To request again the service: h1 python3 client.py {host_server1.IP()})\n")
                    host_server1.cmd('python3 ./Servers/server1.py &')  #start the server
                    time.sleep(3)
                    result = host_client.cmd("python3 client.py " + str(host_server1.IP()))
                    print(result)
                    print("press Enter to continue...")
                    service_started1 = True
                elif stato == "off" and service_started1:
                    print("\nServer1 stopped!\n")
                    host_server1.cmd('pkill -f ./Servers/server1.py &')  #Stop the server
                    print("press Enter to continue...")
                    service_started1 = False
        except Exception as e:
            print(f"Errore nel monitoraggio del file: {e}")
        

        try:
            with open(Directories["serv2"], "r") as file:
                stato = file.read().strip()   #read the file
                if stato == "on" and not service_started2 :
                    print(f"\nStarting Server 2 IP: {host_server2.IP()} on host {host_server2} IP: {host_server2.IP()}...")
                    print(f"\n(To request again the service: h1 python3 client.py {host_server2.IP()})\n")
                    host_server2.cmd('python3 ./Servers/server2.py &')  #start the server
                    time.sleep(3)
                    result = host_client.cmd("python3 client.py " + str(host_server2.IP()))
                    print(result)
                    print("press Enter to continue...")
                    service_started2 = True
                elif stato == "off" and service_started2:
                    print("\nServer2 stopped!\n")
                    host_server1.cmd('pkill -f ./Servers/server2.py &')  #Stop the server
                    print("press Enter to continue...")
                    service_started2 = False
        except Exception as e:
            print(f"Errore nel monitoraggio del file: {e}")
       


        try:
            with open(Directories["serv3"], "r") as file:
                stato = file.read().strip()   #read the file
                if stato == "on" and not service_started3 :
                    print(f"\nStarting Server 3 IP: {host_server3.IP()} on host {host_server3} IP: {host_server3.IP()}...")
                    print(f"\n(To request again the service: h1 python3 client.py {host_server3.IP()})\n")
                    host_server3.cmd('python3 ./Servers/server3.py &')  #start the server
                    time.sleep(3)
                    result = host_client.cmd("python3 client.py " + str(host_server3.IP()))
                    print(result)
                    print("press Enter to continue...")
                    service_started3 = True
                elif stato == "off" and service_started3:
                    print("\nServer3 stopped!\n")
                    host_server3.cmd('pkill -f ./Servers/server3.py &')  #Stop the server
                    print("press Enter to continue...")
                    service_started3 = False
        except Exception as e:
            print(f"Errore nel monitoraggio del file: {e}")
       


        try:
            with open(Directories["serv4"], "r") as file:
                stato = file.read().strip()   #read the file
                if stato == "on" and not service_started4 :
                    print(f"\nStarting Server 4 IP: {host_server4.IP()} on host {host_server4} IP: {host_server4.IP()}...")
                    print(f"\n(To request again the service: h1 python3 client.py {host_server4.IP()})\n")
                    host_server4.cmd('python3 ./Servers/server4.py &')  # english: start the server
                    time.sleep(3)
                    result = host_client.cmd("python3 client.py " + str(host_server4.IP()))
                    print(result)
                    print("press Enter to continue...")
                    service_started4 = True
                elif stato == "off" and service_started4:
                    print("\nServer4 stopped!\n")
                    host_server4.cmd('pkill -f ./Servers/server4.py &')  #Stop the server
                    print("press Enter to continue...")
                    service_started4 = False
        except Exception as e:
            print(f"Errore nel monitoraggio del file: {e}")
        
        time.sleep(1)  #check every second

def run_minimal_network():
    
    # Connect Mininet to the already running Ryu controller at localhost:6653
    c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
    
    # Create the network using the custom topology and connect it to the Ryu controller
    global net
    net = Mininet(topo=MyTopo(), switch=OVSSwitch, controller=c0, autoSetMacs=True)

    # Start the network
    net.start()
    net.staticArp()

    # Start monitoring the file in a separate thread
    monitor_thread = threading.Thread(target=assign_services)
    monitor_thread.daemon = True # This will make the thread terminate when the main program terminates
    monitor_thread.start()

    CLI(net)

    # Stop the network when exiting the CLI
    net.stop()



if __name__ == '__main__': 
    run_minimal_network()


