# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
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
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4
import csv


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        src_port= 1
        temp =1
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src
        #Apri il file server1_path.csv e leggi i dati
        with open('/media/sf_NGN_Project/Servers/server1_path.csv', 'r') as file_path:
            reader=csv.DictReader(file_path)
            # Itera sulle righe del file server1_path.csv
            for row in reader:
                src_switch = row['Source']
                dst_switch = row['Dest.']

                # Ora apri net.csv e leggi i dati
                with open('/media/sf_NGN_Project/net.csv', 'r') as file_net:
                    reader1 = csv.DictReader(file_net)
                    # Itera sulle righe del file net.csv
                    for row1 in reader1:
                        # Verifica se la riga corrisponde tra source e destination
                        if row1['Source'] == str(src_switch) and row1['Dest.'] == str(dst_switch):
                            # Ottieni le porte sorgente e destinazione
                            src_MAC = row1['SrcMAC']
                            print(f"\nswitch source out mac: {src_MAC}")
                            
                            dst_MAC = row1['DstMAC']
                            print(f"\nswitch destination in mac : {dst_MAC}")

                            dst_port = int(row1['SrcPort'].replace('eth', ''))  # Converte la porta in un numero
                            print ("\ndestination port: ", dst_port)

                            src_port = temp  # Converte la porta in un numero
                            print ("\nsource port: ", src_port)

                            temp = int(row1['DstPort'].replace('eth', ''))

                            # Crea un match basato sul MAC address e sulla porta di ingresso
                            #match = parser.OFPMatch(in_port=src_port, eth_dst=dst_MAC)
                            

                            # Aggiungi l'azione per inoltrare il pacchetto sulla porta di destinazione
                            actions = [parser.OFPActionOutput(dst_port)]
                            match = parser.OFPMatch(in_port=src_port, eth_dst=dst, eth_src=src)

                            # Aggiungi il flusso allo switch
                            self.add_flow(datapath, 1, match, actions)


        # if eth.ethertype == ether_types.ETH_TYPE_LLDP:
        #     # ignore lldp packet
        #     return
        

        # dpid = format(datapath.id, "d").zfill(16)
        # self.mac_to_port.setdefault(dpid, {})

        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # # learn a mac address to avoid FLOOD next time.
        # self.mac_to_port[dpid][src] = in_port

        # if dst in self.mac_to_port[dpid]:
        #     out_port = self.mac_to_port[dpid][dst]
        #     self.logger.info("output port for %s is known: %d", dst, out_port)

        # else:
        #     out_port = ofproto.OFPP_FLOOD
        #     self.logger.info("output port for %s is unknown: FLOODING", dst)

        # actions = [parser.OFPActionOutput(out_port)]

        # # install a flow to avoid packet_in next time
        # if out_port != ofproto.OFPP_FLOOD:
        #     match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
        #     # verify if we have a valid buffer_id, if yes avoid to send both
        #     # flow_mod & packet_out
        #     if msg.buffer_id != ofproto.OFP_NO_BUFFER:
        #         self.add_flow(datapath, 1, match, actions, msg.buffer_id)
        #         return
        #     else:
        #         self.add_flow(datapath, 1, match, actions)
        # data = None
        # if msg.buffer_id == ofproto.OFP_NO_BUFFER:
        #     data = msg.data

        # out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
        #                           in_port=in_port, actions=actions, data=data)
        # datapath.send_msg(out)


