#!/usr/bin/env python
# coding=utf-8

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
import time


class MyTopo(Topo):
    "Rete minima con due switch e due host."

    def build(self):  
        
        # Aggiungi due host
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
     
       
       
        # Aggiungi uno switch
        s1 = self.addSwitch('s1',protocols='OpenFlow13', stp = True)
        s2 = self.addSwitch('s2',protocols='OpenFlow13', stp = True)
        s3 = self.addSwitch('s3',protocols='OpenFlow13', stp = True)
        s4 = self.addSwitch('s4',protocols='OpenFlow13', stp = True)
        
        #Aggiungi i link
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h4, s4)
        self.addLink(h3, s3)

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        # self.addLink(s4, s1)

        
        


def run_minimal_network():
    # Connect Mininet to the already running Ryu controller at localhost:6653
    c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
    
    # Create the network using the custom topology and connect it to the Ryu controller
    net = Mininet(topo=MyTopo(), switch=OVSSwitch, controller=c0)
    
    # Start the network
    net.start()
    time.sleep(5)
    # (Optional) Verify connectivity between hosts
    print("Testing connectivity...try:")
    print("h1 ping -c 1 h2")
    # net.pingAll()

    # Start the CLI for manual interaction
    CLI(net)

    # Stop the network when exiting the CLI
    net.stop()

if __name__ == '__main__':
    run_minimal_network()
