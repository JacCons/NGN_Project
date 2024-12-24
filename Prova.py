from mininet.net import Mininet

# Creazione rete
net = Mininet()
h1 = net.addHost('h1')  # h1 è un oggetto Host
h2 = net.addHost('h2')  # h2 è un oggetto Host
s1 = net.addSwitch('s1')
net.addLink(h1, s1)
net.addLink(h2, s1)

# Avvio rete
net.start()

# Esecuzione di comandi sugli host
print(h1.cmd('ifconfig'))  # Corretto, h1 è un oggetto Host
print(h2.cmd('ping -c 3 10.0.0.1'))  # Corretto

# Arresto rete
net.stop()
