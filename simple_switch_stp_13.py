# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import dpid as dpid_lib
from ryu.lib import stplib
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.app import simple_switch_13
#import  socket
#import json 
import csv


# from ryu.ofproto import ofproto_v1_3

# def install_path(self, path, src_host, dst_host):
#     """   
#     Installa il percorso più breve tra i due host, utilizzando gli indirizzi IP.
#     :param path: Lista di switch lungo il percorso
#     :param src_host: Nome host di partenza
#     :param dst_host: Nome host di destinazione
#     """
#     src_ip = self.get_ip_of_host(src_host)
#     dst_ip = self.get_ip_of_host(dst_host)
    
#     for i in range(len(path) - 1):
#         datapath = self.get_datapath(path[i])
#         next_hop = path[i + 1]
#         out_port = self.topology[path[i]][next_hop]

#         # Installa il flusso
#         self.update_flow(datapath, src_ip, dst_ip, out_port)


# #Set up the server
# HOST = '127.0.0.1'  # Localhost
# PORT = 10000        # Port to listen on

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#     server_socket.bind((HOST, PORT))
#     server_socket.listen()
#     print(f"Server listening on {HOST}:{PORT}")
    
#     conn, addr = server_socket.accept()
#     with conn:
#         # print(f"Connected by {addr}")
#         # Receive data
#         data = conn.recv(1024)  # Buffer size
#         if data:
#             Date_time_path = json.loads(data.decode('utf-8'))
#             print(f"Received variable: {Date_time_path}")


class SimpleSwitch13(simple_switch_13.SimpleSwitch13):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'stplib': stplib.Stp}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.stp = kwargs['stplib']

        # Sample of stplib config.
        #  please refer to stplib.Stp.set_config() for details.
        config = {dpid_lib.str_to_dpid('0000000000000001'):
                  {'bridge': {'priority': 0x8000}},
                  dpid_lib.str_to_dpid('0000000000000002'):
                  {'bridge': {'priority': 0x9000}},
                  dpid_lib.str_to_dpid('0000000000000003'):
                  {'bridge': {'priority': 0xa000}}}
        self.stp.set_config(config)

    def delete_flow(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        for dst in self.mac_to_port[datapath.id].keys():
            match = parser.OFPMatch(eth_dst=dst)
            mod = parser.OFPFlowMod(
                datapath, command=ofproto.OFPFC_DELETE,
                out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY,
                priority=1, match=match)
            datapath.send_msg(mod)

    def load_links(self, filename):
        """Carica i collegamenti da un file CSV in un dizionario."""
        link_ports = {}
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                src = row['Source']
                dst = row['Destination']
                src_port = int(row['SrcPort'].replace('eth', ''))  # Rimuove "eth" se necessario
                dst_port = int(row['DstPort'].replace('eth', ''))
                link_ports[(src, dst)] = (src_port, dst_port)
        return link_ports

    @set_ev_cls(stplib.EventPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg #contains the packet that was sent to the controller and details
        datapath = msg.datapath #contains the switch that sent the packet
        ofproto = datapath.ofproto #contains the OpenFlow protocol version used by the switch
        parser = datapath.ofproto_parser #contains the OpenFlow protocol parser

        in_port = msg.match['in_port'] #contains the switch port number that the packet was received on

        pkt = packet.Packet(msg.data) #extracts the content of the packet
        eth = pkt.get_protocols(ethernet.ethernet)[0] #extracts the Ethernet header from the packet

        dst = eth.dst #contains the destination MAC address of the packet
        src = eth.src #contains the source MAC address of the packet

        dpid = datapath.id #contains the datapath ID of the switch that sent the packet
        self.mac_to_port.setdefault(dpid, {}) #creates a dictionary for the switch if it does not exist

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        #self.mac_to_port[dpid][src] = in_port #stores the source MAC address and the port number that the packet was received on
        # with open('/media/sf_NGN_Project/Servers/server1_path.csv', 'r') as file_path:
        #     for row in file_path:
        #         src_switch = row['Source']
        #         dst_switch = row['Destination']
        #         src_MAC = row['SrcMAC']
        #         dst_MAC = row['DstMAC']
        #         with open ('/media/sf_NGN_Project/net.csv', 'r') as file_net:
        #             for row in file_net:
        #                 if row['Source'] == src_switch and row['Dest.'] == dst_switch:
        #             # Se la riga corrisponde, otteniamo src_port e dst_port
        #                     src_port = int(row['SrcPort'].replace('eth', ''))
        #                     dst_port = int(row['DstPort'].replace('eth', ''))
        #                     actions = [parser.OFPActionOutput(dst_port)]
        #                     #actions = [parser.OFPActionOutput(dst_port)]#contains the action to be performed on the packet
        #                     # match = parser.OFPMatch(in_port=in_port, eth_dst=dst)#creates a match rule 
        #                     # self.add_flow(datapath, 1, match, actions) #adds the flow to the switch
        #                     # self.add_flow(datapath, 1, match, actions) #adds the flow to the switch
        #                     match = parser.OFPMatch(in_port=src_port, eth_dst=dst_MAC)

        #                     # Aggiungi l'azione per inoltrare il pacchetto sulla porta di destinazione
        #                     actions = [parser.OFPActionOutput(dst_port)]

        #                     # Aggiungi il flusso allo switch
        #                     self.add_flow(datapath, 1, match, actions)
    # Apri il file server1_path.csv e leggi i dati
        with open('/media/sf_NGN_Project/Servers/server1_path.csv', 'r') as file_path:
            reader = csv.DictReader(file_path)  # Usa DictReader per leggere il CSV come dizionario

            # Itera sulle righe del file server1_path.csv
            for row in reader:
                src_switch = row['Source']
                dst_switch = row['Dest.']

                # Ora apri net.csv e leggi i dati
                with open('/media/sf_NGN_Project/net.csv', 'r') as file_net:
                    net_reader = csv.DictReader(file_net)

                    # Itera sulle righe del file net.csv
                    for net_row in net_reader:
                        # Verifica se la riga corrisponde tra source e destination
                        if net_row['Source'] == src_switch and net_row['Dest.'] == dst_switch:
                            # Ottieni le porte sorgente e destinazione
                            src_MAC = row['SrcMAC']
                            dst_MAC = row['DstMAC']
                            src_port = int(net_row['SrcPort'].replace('eth', ''))  # Converte la porta in un numero
                            dst_port = int(net_row['DstPort'].replace('eth', ''))  # Converte la porta in un numero
                            
                            # Crea un match basato sul MAC address e sulla porta di ingresso
                            match = parser.OFPMatch(in_port=src_port, eth_dst=dst_MAC)

                            # Aggiungi l'azione per inoltrare il pacchetto sulla porta di destinazione
                            actions = [parser.OFPActionOutput(dst_port)]

                            # Aggiungi il flusso allo switch
                            self.add_flow(datapath, 1, match, actions)





    #We commented this part to avoid switches from communicating when starting the controller
        # if dst in self.mac_to_port[dpid]:
        #     out_port = self.mac_to_port[dpid][dst]
        # else:
        #     out_port = ofproto.OFPP_FLOOD

        # actions = [parser.OFPActionOutput(out_port)]#contains the action to be performed on the packet
        # #in this case forward packet to out port

        # # install a flow to avoid packet_in next time
        # if out_port != ofproto.OFPP_FLOOD:
        #     match = parser.OFPMatch(in_port=in_port, eth_dst=dst)#creates a match rule 
        #     self.add_flow(datapath, 1, match, actions) #adds the flow to the switch

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    @set_ev_cls(stplib.EventTopologyChange, MAIN_DISPATCHER)
    def _topology_change_handler(self, ev):
        dp = ev.dp
        dpid_str = dpid_lib.dpid_to_str(dp.id)
        msg = 'Receive topology change event. Flush MAC table.'
        self.logger.debug("[dpid=%s] %s", dpid_str, msg)

        if dp.id in self.mac_to_port:
            self.delete_flow(dp)
            del self.mac_to_port[dp.id]

    @set_ev_cls(stplib.EventPortStateChange, MAIN_DISPATCHER)
    def _port_state_change_handler(self, ev):
        dpid_str = dpid_lib.dpid_to_str(ev.dp.id)
        of_state = {stplib.PORT_STATE_DISABLE: 'DISABLE',
                    stplib.PORT_STATE_BLOCK: 'BLOCK',
                    stplib.PORT_STATE_LISTEN: 'LISTEN',
                    stplib.PORT_STATE_LEARN: 'LEARN',
                    stplib.PORT_STATE_FORWARD: 'FORWARD'}
        self.logger.debug("[dpid=%s][port=%d] state=%s",
                          dpid_str, ev.port_no, of_state[ev.port_state])
