import time
import threading
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI

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


def run_minimal_network():
    # Connetti Mininet al controller Ryu su localhost:6653
    c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
    
    # Crea la rete con la topologia personalizzata e il controller Ryu
    net = Mininet(topo=MyTopo(), switch=OVSSwitch, controller=c0)
    
    # Avvia la rete
    net.start()
    print("Rete avviata.")
    
    # Attendi la convergenza di STP
    #wait_for_stp_convergence(timeout=3)

    # Recupera gli host dalla rete
    h1 = net.get('h1')  # Ottieni oggetto host h1
    h2 = net.get('h2')  # Ottieni oggetto host h2

    # Verifica connessione con ping
    # print("Testing connectivity between hosts...")
    # if net.ping([h1, h2]) > 0:
    #     print("Ping failed after STP convergence. Exiting.")
    #     net.stop()
    #     return

    switch = net.get('s1')
    first_intf = list(switch.intfs.values())[0]
    MAC = first_intf.MAC()
    print(MAC)
    # Ottieni la prima interfaccia disponibile dello switch


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

