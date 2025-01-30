from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import dpid as dpid_lib
from ryu.lib import stplib
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.app import simple_switch_13

from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from webob import Response


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
        config = {dpid_lib.str_to_dpid('0000000000000001'):
                  {'bridge': {'priority': 0x8000}},
                  dpid_lib.str_to_dpid('0000000000000002'):
                  {'bridge': {'priority': 0x9000}},
                  dpid_lib.str_to_dpid('0000000000000003'):
                  {'bridge': {'priority': 0xa000}}}
        self.stp.set_config(config)

    # default function to delete function
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

    # new implementation for the NGN project. 
    # it deletes all the flows between the host h1 and the servers h3, h4, h6, h7
    def delete_flood_flows(self):
        print("\nRequesting flow stats to delete flood flows\n")

        for dp in self.datapaths.values():
            print(f"Requesting flow stats from switch {dp.id}\n")
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

    # takes the packet and checks if it is between h1 and h3, h4, h6, h7 and adds the flow.
    # it comunicates with the controller to add the flows between h1 and the servers
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

        # MAC address of h1 and h3
        h1_mac = '00:00:00:00:00:01'  # MAC di h1
        h3_mac = '00:00:00:00:00:03'  # MAC di h3
        h4_mac = '00:00:00:00:00:04'  # MAC di h4
        h6_mac = '00:00:00:00:00:06'  # MAC di h6
        h7_mac = '00:00:00:00:00:07'  # MAC di h7

       

        # If the packet is between h1 and h3, add a specific flow
        if (src == h1_mac and dst == h3_mac) or (src == h3_mac and dst == h1_mac): 
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
            self.logger.info("Adding flow for h1 and h3 communication")

            # Create the match for the traffic between h1 and h3
            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            # Find the correct port to use
            out_port = self.mac_to_port[dpid].get(dst) # Get the output port for the destination

            if out_port is not None:
                # Action: send the packet to the specific port
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                # If there is no port for the destination, it can be a "not recognized" packet (flooding)
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)

        # If the packet is between h1 and h4, add a specific flow
        if (src == h1_mac and dst == h4_mac) or (src == h4_mac and dst == h1_mac):
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

            self.logger.info("Adding flow for h1 and h4 communication")

            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            out_port = self.mac_to_port[dpid].get(dst)

            if out_port is not None:
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)
                
        # If the packet is between h1 and h6, add a specific flow
        if (src == h1_mac and dst == h6_mac) or (src == h6_mac and dst == h1_mac):
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

            self.logger.info("Adding flow for h1 and h6 communication")

            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            out_port = self.mac_to_port[dpid].get(dst)

            if out_port is not None:
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)

        # If the packet is between h1 and h7, add a specific flow
        if (src == h1_mac and dst == h7_mac) or (src == h7_mac and dst == h1_mac):
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

            self.logger.info("Adding flow for h1 and h7 communication")

            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            out_port = self.mac_to_port[dpid].get(dst)

            if out_port is not None:
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)
                
        # If the packet is between h3 and h7, add a specific flow
        if (src == h3_mac and dst == h7_mac) or ( src == h7_mac and dst == h3_mac):
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

            self.logger.info("Adding flow for h3 and h7 communication")

            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)

            out_port = self.mac_to_port[dpid].get(dst)

            if out_port is not None:
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
            else:
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                self.add_flow(datapath, 1, match, actions)

    # Function to handle the topology change
    @set_ev_cls(stplib.EventTopologyChange, MAIN_DISPATCHER)
    def _topology_change_handler(self, ev):
        dp = ev.dp
        dpid_str = dpid_lib.dpid_to_str(dp.id)
        msg = 'Receive topology change event. Flush MAC table.'
        self.logger.debug("[dpid=%s] %s", dpid_str, msg)

        if dp.id in self.mac_to_port:
            self.delete_flow(dp)
            del self.mac_to_port[dp.id]

    # Function to handle the port state change
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

# Class that extends the controller and through REST API communicates when to delete the flows
class SimpleSwitch13Controller(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SimpleSwitch13Controller, self).__init__(req, link, data, **config)
        self.simple_switch_app = data['simple_switch_app']
    
    @route('simple_switch', '/simpleswitch/delete_flood_flows', methods=['POST'])
    def delete_flows(self, req, **kwargs):
        self.simple_switch_app.delete_flood_flows()
        return Response(status=200, body="All flows deleted")
