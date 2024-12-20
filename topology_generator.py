import networkx as nx
import matplotlib.pyplot as plt
import random
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, OVSController
#ssh -X -p 2222 vagrant@localhost

class MyTopo (Topo):
    
    def gen_topology(self):
        
        n_host = 8
        n_switch = 7
        hosts_NODES=[]
        hosts_MN=[] #array of hosts
        switch_NODES=[]
        switch_MN=[] #array of switches
        link_NODES = []
        # Creazione del grafo
        G = nx.Graph()

        # Aggiunta dei nodi host
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
            switch_MN.append(self.addSwitch(switchname,protocols='OpenFlow13'))
        G.add_nodes_from(switch_NODES, type="switch")
        
        #Print all switches
        print ("----Switches----")
        print (switch_NODES)
        print("\n")

        # Connessioni casuali tra host e switch
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
        #for cycle from 0 to the second-to-last switch
        for i in range (n_switch-2):
            #print("--------")
            #clear the temporary array
            temp.clear()
            #assign to switch 1 the selected seitch in switch_NODES
            switch1 = switch_NODES[i]
            #random number of non adjacent (+2) links a switch can have
            n_links= random.randint(0,n_switch-(i+2)) 
            
            #print (f"N= {n_links}")
            
            #fill the temporary array [OK]
            for m in range (i+2, n_switch):
                temp.append(switch_NODES[m])
            
            #print(temp)
            
            #create the new links
            for k in range (n_links):
                #select a random switch in the temp list
                switch2 = random.choice(temp)
                #print(switch2)
                #remove the selected switch from the temp list to avoid having duplicate links
                temp.remove(switch2)
                #print(temp)
                self.addLink(switch1, switch2)
                link_NODES.append (f"({switch1},{switch2})") #to print when starting the mininet
                G.add_edge(switch1, switch2)
        
        #Print links
        print ("----Links----")
        print(link_NODES)
        print("\n")
            

        # Disegno del grafo
        pos = nx.spring_layout(G)  # Layout per una visualizzazione più chiara
        colors = ["red" if G.nodes[node]['type'] == "host" else "blue" for node in G.nodes]
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, font_size=10)
        plt.show()

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
            for link in switch.links:
                if link.intf1.node.name == switch.name:
                    neighbor_switch = link.intf2.node.name
                else:
                    neighbor_switch = link.intf1.node.name
                switch_connections[switch.name][neighbor_switch] = 1  # Unit weight for simplicity

        # Create a networkx graph
        graph = nx.Graph(switch_connections)

        # Get source and destination switch names
        src_switch = src_host.connections[0].intf1.node.name
        dst_switch = dst_host.connections[0].intf1.node.name

        # Calculate shortest path using Dijkstra's algorithm
        shortest_path = nx.shortest_path(graph, source=src_switch, target=dst_switch)

        return shortest_path


def run_minimal_network():
    "Crea la rete minima e avvia la CLI."
    # Crea la rete usando la topologia minimale
    c1 = Controller('c0', controller=OVSController)
    net = Mininet(topo=MyTopo(), switch=OVSSwitch, controller=c1)
    
    # Avvia la rete
    net.start()

    # Verifica connettività (opzionale)
    print("Eseguo un ping tra gli host...")
    net.pingAll()

    # Avvia la CLI per interazione manuale
    CLI(net)

    # Assuming you have references to the host objects (h1, h2)
    h1 = net.get('h1')
    h2 = net.get('h2')
    shortest_path = MyTopo.get_shortest_path(net, h1, h2)
    print(f"Shortest path between h1 and h2: {shortest_path}")

    # Ferma la rete quando esci dalla CLI
    net.stop()

if __name__ == '__main__':
    topo = MyTopo() #create a Mytopo object
    topo.gen_topology() 
    run_minimal_network()


