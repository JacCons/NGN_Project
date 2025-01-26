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
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from webob import Response


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
    _CONTEXTS = {'stplib': stplib.Stp, 'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.stp = kwargs['stplib']
        self.datapaths = {}  # Add this line to store datapaths
        self.wsgi = kwargs['wsgi']
        self.wsgi.register(SimpleSwitch13Controller, {'simple_switch_app': self})

        # Sample of stplib config.
        #  please refer to stplib.Stp.set_config() for details.
        config = {dpid_lib.str_to_dpid('0000000000000001'):
                  {'bridge': {'priority': 0x8000}},
                  dpid_lib.str_to_dpid('0000000000000002'):
                  {'bridge': {'priority': 0x9000}},
                  dpid_lib.str_to_dpid('0000000000000003'):
                  {'bridge': {'priority': 0xa000}}}
        self.stp.set_config(config)

    # @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    # def switch_features_handler(self, ev):
    #     datapath = ev.msg.datapath
    #     dpid = datapath.id
    #     self.datapaths[dpid] = datapath
    #     self.logger.info(f"Switch connected: dpid={dpid}")

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

    def delete_all_flows(self):
        print("\nDeleting all flows\n")

        for dp in self.datapaths.values():
            print(f"Deleting flows from switch {dp.id}\n")
            ofproto = dp.ofproto
            parser = dp.ofproto_parser

            # Delete all existing flows
            match = parser.OFPMatch()  # Match all packets
            mod = parser.OFPFlowMod(
                datapath=dp,
                command=ofproto.OFPFC_DELETE,
                out_port=ofproto.OFPP_ANY,
                out_group=ofproto.OFPG_ANY,
                priority=0,
                match=match
            )
            dp.send_msg(mod)

        print("\nAll flows deleted\n")

    def delete_flood_flows(self):
        print("\nRequesting flow stats to delete flood flows\n")

        for dp in self.datapaths.values():
            print(f"Requesting flow stats from switch {dp.id}\n")
            ofproto = dp.ofproto
            parser = dp.ofproto_parser

            # Request flow stats
            req = parser.OFPFlowStatsRequest(datapath=dp)
            dp.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        dp = ev.msg.datapath
        ofproto = dp.ofproto
        parser = dp.ofproto_parser

        for stat in body:
            for instruction in stat.instructions:
                if isinstance(instruction, parser.OFPInstructionActions):
                    if any(isinstance(action, parser.OFPActionOutput) and action.port == ofproto.OFPP_FLOOD for action in instruction.actions):
                        print(f"Deleting flow with FLOOD action from switch {dp.id}\n")
                        # Delete the flow
                        match = stat.match
                        mod = parser.OFPFlowMod(
                            datapath=dp,
                            command=ofproto.OFPFC_DELETE,
                            out_port=ofproto.OFPP_ANY,
                            out_group=ofproto.OFPG_ANY,
                            priority=0,
                            match=match
                        )
                        dp.send_msg(mod)

        print("\nAll flood flows deleted\n")




    # @set_ev_cls(stplib.EventPacketIn, MAIN_DISPATCHER)
    # def _packet_in_handler(self, ev):
    #     src_port= 1
    #     temp =1
    #     msg = ev.msg #contains the packet that was sent to the controller and details
    #     datapath = msg.datapath #contains the switch that sent the packet
    #     ofproto = datapath.ofproto #contains the OpenFlow protocol version used by the switch
    #     parser = datapath.ofproto_parser #contains the OpenFlow protocol parser

    #     in_port = msg.match['in_port'] #contains the switch port number that the packet was received on

    #     pkt = packet.Packet(msg.data) #extracts the content of the packet
    #     eth = pkt.get_protocols(ethernet.ethernet)[0] #extracts the Ethernet header from the packet

    #     dst = eth.dst #contains the destination MAC address of the packet
    #     src = eth.src #contains the source MAC address of the packet

    #     dpid = datapath.id #contains the datapath ID of the switch that sent the packet
    #     self.mac_to_port.setdefault(dpid, {}) #creates a dictionary for the switch if it does not exist

    #     self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

    #     # #learn a mac address to avoid FLOOD next time.
    #     # self.mac_to_port[dpid][src] = in_port #stores the source MAC address and the port number that the packet was received on
        
    # #Apri il file server1_path.csv e leggi i dati
    #     with open('/media/sf_NGN_Project/Servers/server1_path.csv', 'r') as file_path:
    #         reader=csv.DictReader(file_path)
    #         # Itera sulle righe del file server1_path.csv
    #         for row in reader:
    #             src_switch = row['Source']
    #             dst_switch = row['Dest.']

    #             # Ora apri net.csv e leggi i dati
    #             with open('/media/sf_NGN_Project/net.csv', 'r') as file_net:
    #                 reader1 = csv.DictReader(file_net)
    #                 # Itera sulle righe del file net.csv
    #                 for row1 in reader1:
    #                     # Verifica se la riga corrisponde tra source e destination
    #                     if row1['Source'] == str(src_switch) and row1['Dest.'] == str(dst_switch):
    #                         # Ottieni le porte sorgente e destinazione
    #                         src_MAC = row1['SrcMAC']
    #                         print(f"\nsource mac: {src_MAC}")
                            
    #                         dst_MAC = row1['DstMAC']
    #                         print(f"\ndestination mac: {dst_MAC}")

    #                         dst_port = int(row1['SrcPort'].replace('eth', ''))  
    #                         print ("\ndestination port: ", dst_port)

    #                         src_port = temp  
    #                         print ("\nsource port: ", src_port)

    #                         temp = int(row1['DstPort'].replace('eth', ''))

    #                         src_dpid = int(src_switch.replace('s', ''))  # Assumendo che gli switch siano nominati "s1", "s2", ecc.
    #                         datapath = self.datapaths.get(src_dpid)

    #                         # Crea un match basato sul MAC address e sulla porta di ingresso
    #                         #match = parser.OFPMatch(in_port=src_port, eth_dst=dst_MAC)
    #                         match = parser.OFPMatch(in_port=src_port, eth_dst=src_MAC, eth_src=dst_MAC)
    #                         # Aggiungi l'azione per inoltrare il pacchetto sulla porta di destinazione
    #                         actions = [parser.OFPActionOutput(dst_port)]

    #                         # Aggiungi il flusso allo switch
    #                         self.add_flow(datapath, 1, match, actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        self.datapaths[datapath.id] = datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        src = eth.src
        dst = eth.dst

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # Indirizzi MAC di h1 e h3 (sostituisci con gli indirizzi corretti)
        h1_mac = '00:00:00:00:00:01'  # MAC di h1
        h3_mac = '00:00:00:00:00:03'  # MAC di h3
        h4_mac = '00:00:00:00:00:04'  # MAC di h4
        h6_mac = '00:00:00:00:00:06'  # MAC di h6
        h7_mac = '00:00:00:00:00:07'  # MAC di h7

        # Log del pacchetto ricevuto
       

        # Se il pacchetto è tra h1 e h3, aggiungi un flusso specifico
        if (src == h1_mac and dst == h3_mac) or (src == h3_mac and dst == h1_mac): 
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
            self.logger.info("Adding flow for h1 and h3 communication")

            # Creazione del match per il traffico tra h1 e h3
            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            # Trova la porta corretta da usare
            out_port = self.mac_to_port[dpid].get(dst)  # Ottieni la porta di uscita per il destinatario

            if out_port is not None:
                # Azione: invia il pacchetto alla porta specifica
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)

        if (src == h1_mac and dst == h4_mac) or (src == h4_mac and dst == h1_mac):
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

            self.logger.info("Adding flow for h1 and h4 communication")

            # Creazione del match per il traffico tra h1 e h4
            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            # Trova la porta corretta da usare
            out_port = self.mac_to_port[dpid].get(dst)

            if out_port is not None:
                # Azione: invia il pacchetto alla porta specifica
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)

        if (src == h1_mac and dst == h6_mac) or (src == h6_mac and dst == h1_mac):
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

            self.logger.info("Adding flow for h1 and h6 communication")

            # Creazione del match per il traffico tra h1 e h6
            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            # Trova la porta corretta da usare
            out_port = self.mac_to_port[dpid].get(dst)

            if out_port is not None:
                # Azione: invia il pacchetto alla porta specifica
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)


        if (src == h1_mac and dst == h7_mac) or (src == h7_mac and dst == h1_mac):
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

            self.logger.info("Adding flow for h1 and h7 communication")

            # Creazione del match per il traffico tra h1 e h7
            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            # Trova la porta corretta da usare
            out_port = self.mac_to_port[dpid].get(dst)

            if out_port is not None:
                # Azione: invia il pacchetto alla porta specifica
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)
        
        if (src == h3_mac and dst == h7_mac) or ( src == h7_mac and dst == h3_mac):
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

            self.logger.info("Adding flow for h3 and h7 communication")

            # Creazione del match per il traffico tra h3 e h7
            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            # Trova la porta corretta da usare
            out_port = self.mac_to_port[dpid].get(dst)

            if out_port is not None:
                # Azione: invia il pacchetto alla porta specifica
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)
                
        # if(src == h3_mac and dst == h7_mac) or (src == h7_mac and dst == h3_mac):
        #     self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        #     self.logger.info("Adding flow for h3 and h7 communication")

        #     # Creazione del match per il traffico tra h3 e h7
        #     match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

        #     # Trova la porta corretta da usare
        #     out_port = self.mac_to_port[dpid].get(dst)

        #     if out_port is not None:
        #         # Azione: invia il pacchetto alla porta specifica
        #         actions = [parser.OFPActionOutput(out_port)]
        #         self.add_flow(datapath, 1, match, actions)
        #     else:
        #         # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
        #         actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        #         self.add_flow(datapath, 1, match, actions)


        # if (src == h1_mac and dst == h7_mac) or (src == h7_mac and dst == h1_mac) or (src == h3_mac and dst == h7_mac) or (src == h7_mac and dst == h3_mac):

        #     match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

        #     if(src == h1_mac):
        #         self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        #         self.logger.info("Adding flow for h1 and h3 communication")

        #         # Creazione del match per il traffico tra h1 e h3
        #         match = parser.OFPMatch(in_port=in_port, eth_src=h1_mac, eth_dst=h3_mac)
        #         out_port = self.mac_to_port[dpid].get(dst)  # Ottieni la porta di uscita per il destinatario

        #         if out_port is not None:
        #             # Azione: invia il pacchetto alla porta specifica
        #             actions = [parser.OFPActionOutput(out_port)]
        #             self.add_flow(datapath, 1, match, actions)
        #         else:
        #             # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
        #             actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        #             self.add_flow(datapath, 1, match, actions)

        #     if(src == h3_mac):
        #         self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        #         self.logger.info("Adding flow for h3 and h7 communication")

        #         # Creazione del match per il traffico tra h1 e h3
        #         match = parser.OFPMatch(in_port=in_port, eth_src=h3_mac, eth_dst=h7_mac)
        #         out_port = self.mac_to_port[dpid].get(dst)  # Ottieni la porta di uscita per il destinatario

        #         if out_port is not None:
        #             # Azione: invia il pacchetto alla porta specifica
        #             actions = [parser.OFPActionOutput(out_port)]
        #             self.add_flow(datapath, 1, match, actions)
        #         else:
        #             # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
        #             actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        #             self.add_flow(datapath, 1, match, actions)
            
        #     if( src == h1_mac and dst == h7_mac ):
        #         self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        #         self.logger.info("Adding flow for h1 and h3 communication - src h1 and dst h7")

        #         # Creazione del match per il traffico tra h1 e h3
        #         match = parser.OFPMatch(in_port=in_port, eth_src=h1_mac, eth_dst=h3_mac)
        #         # Trova la porta corretta da usare
        #         out_port = self.mac_to_port[dpid].get(dst)

        #         if out_port is not None:
        #             # Azione: invia il pacchetto alla porta specifica
        #             actions = [parser.OFPActionOutput(out_port)]
        #             self.add_flow(datapath, 1, match, actions)
        #         else:
        #             # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
        #             actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        #             self.add_flow(datapath, 1, match, actions)

        #     if( src == h7_mac and dst == h1_mac ):
        #         self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        #         self.logger.info("Adding flow for h1 and h7 communication")

        #         # Creazione del match per il traffico tra h1 e h3
        #         match = parser.OFPMatch(in_port=in_port, eth_src=h7_mac, eth_dst=h1_mac)
        #         out_port = self.mac_to_port[dpid].get(dst)  # Ottieni la porta di uscita per il destinatario

        #         if out_port is not None:
        #             # Azione: invia il pacchetto alla porta specifica
        #             actions = [parser.OFPActionOutput(out_port)]
        #             self.add_flow(datapath, 1, match, actions)
        #         else:
        #             # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
        #             actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        #             self.add_flow(datapath, 1, match, actions)

            # if (src == h7_mac):
            #     self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
            #     self.logger.info("Adding flow for h7 and h1 communication")

            #     # Creazione del match per il traffico tra h1 e h3
            #     match = parser.OFPMatch(in_port=in_port, eth_src=h7_mac, eth_dst=h3_mac)

            # if (src == h3_mac):
            #     self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
            #     self.logger.info("Adding flow for h7 and h1 communication")

            #     # Creazione del match per il traffico tra h1 e h3
            #     match = parser.OFPMatch(in_port=in_port, eth_src=h3_mac, eth_dst=h1_mac)

                
            # Trova la porta corretta da usare            
            # out_port = self.mac_to_port[dpid].get(dst)  # Ottieni la porta di uscita per il destinatario

            # if out_port is not None:
            #     # Azione: invia il pacchetto alla porta specifica
            #     actions = [parser.OFPActionOutput(out_port)]
            #     self.add_flow(datapath, 1, match, actions)
            # else:
            #     # Se non c'è una porta per il destinatario, può essere un pacchetto "not recognized" (flooding)
            #     actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
            #     self.add_flow(datapath, 1, match, actions)
        # else:
        #     self.logger.info(f"Dropping packet not between src: {src} and dst: {dst}")

                           



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

        # data = None
        # if msg.buffer_id == ofproto.OFP_NO_BUFFER:
        #     data = msg.data

        # out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
        #                           in_port=in_port, actions=actions, data=data)
        # datapath.send_msg(out)


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

# Classe che estende il controllore e attraverso REST API comunica quando eliminare i flows
class SimpleSwitch13Controller(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SimpleSwitch13Controller, self).__init__(req, link, data, **config)
        self.simple_switch_app = data['simple_switch_app']

    @route('simple_switch', '/simpleswitch/delete_flows', methods=['POST'])
    def delete_flows(self, req, **kwargs):
        self.simple_switch_app.delete_all_flows()
        return Response(status=200, body="All flows deleted")
    
    @route('simple_switch', '/simpleswitch/delete_flood_flows', methods=['POST'])
    def delete_flows(self, req, **kwargs):
        self.simple_switch_app.delete_flood_flows()
        return Response(status=200, body="All flows deleted")
