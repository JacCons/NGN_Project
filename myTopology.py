#!/usr/bin/env python
# coding=utf-8

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, OVSController

class MinimalTopo(Topo):
    "Rete minima con due switch e due host."

    def build(self):
        
        
        # Aggiungi due host
        h1 = self.addHost('h1',mac='00:00:00:00:00:01')
        h2 = self.addHost('h2',mac='00:00:00:00:00:02')
       
       
        # Aggiungi uno switch
        s1 = self.addSwitch('s1',protocols='OpenFlow13')
        s2 = self.addSwitch('s2',protocols='OpenFlow13')
        
        #Aggiungi i link
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(s1, s2)


def run_minimal_network():
    "Crea la rete minima e avvia la CLI."
    # Crea la rete usando la topologia minimale
    #c1 = Controller('c0', controller=OVSController, port=6653)
    net = Mininet(topo=MinimalTopo(), switch=OVSSwitch)
    
    # Avvia la rete
    net.start()

    # Verifica connettività (opzionale)
    print("Eseguo un ping tra gli host...")
    net.pingAll()

    # Avvia la CLI per interazione manuale
    CLI(net)

    # Ferma la rete quando esci dalla CLI
    net.stop()

if __name__ == '__main__':
    run_minimal_network()

