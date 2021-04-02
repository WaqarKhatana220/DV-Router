import sys
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads


class DVrouter(Router):
    """Distance vector routing protocol implementation."""

    def __init__(self, addr, heartbeatTime):
        """TODO: add your own class fields and initialization code here"""
        Router.__init__(self, addr)  # initialize superclass - don't remove
        self.heartbeatTime = heartbeatTime
        self.last_time = 0
        # Hints: initialize local state
        self.addr = addr
        self.distance_vector = {self.addr:0}
        self.forwarding_table = {self.addr:[0, 0, 0]}
        self.neighbours = {}

    def broadcast_to_neighbours(self):
        # self.printer()
        for dest_addresses in self.neighbours:
            packet = Packet("ROUTING", self.addr, dest_addresses, dumps(self.distance_vector))
            self.send(self.neighbours[dest_addresses], packet)

    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""
        if packet.isTraceroute():
            # Hints: this is a normal data packet
            # if the forwarding table contains packet.dstAddr
            #   send packet based on forwarding table, e.g., self.send(port, packet)
            # print("type: TRACEROUTE", "port:", port, "packet:", packet , "content:", packet.getContent(), "src addr:", packet.srcAddr, "dst Addr:", packet.dstAddr, "my addr:", self.addr)
            packet_dest_addr = packet.dstAddr
            for dest_addresses in self.forwarding_table:
                if dest_addresses == packet_dest_addr:
                    self.send(self.forwarding_table[dest_addresses][2], packet)


        else:
            # Hints: this is a routing packet generated by your routing protocol
            # if the received distance vector is different
            #   update the local copy of the distance vector
            #   update the distance vector of this router
            #   update the forwarding table
            #   broadcast the distance vector of this router to neighbors
            # print("packet is routing, printing content")
            # print("port:", port, "content", packet.getContent(), "src addr:", packet.srcAddr, "dstAddr:", packet.dstAddr)
            incoming_dist_vector = loads(packet.getContent())
            # print("type: ROUTING", "port:", port, "packet:", packet , "content:", packet.getContent(), "src addr:", packet.srcAddr, "dst Addr:", packet.dstAddr, "my addr:", self.addr)
            # print("incoming_dist_vector:", incoming_dist_vector)
            for dests in incoming_dist_vector:
                if dests in self.distance_vector:
                    if self.distance_vector[dests] > incoming_dist_vector[dests]:
                        new_cost = incoming_dist_vector[dests] + 1
                        self.distance_vector[dests] = new_cost
                        self.forwarding_table[dests] = [new_cost, packet.srcAddr, port]
                        #self.broadcast_to_neighbours()

                else:
                    new_cost = incoming_dist_vector[dests] + 1
                    self.distance_vector[dests] = new_cost
                    self.forwarding_table[dests] = [new_cost, packet.srcAddr, port]
                    # self.broadcast_to_neighbours()
             
                        
                      


            


    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        # update the distance vector of this router
        # update the forwarding table
        # broadcast the distance vector of this router to neighbors
        addr = endpoint
        next_hop = endpoint
        self.forwarding_table[addr] = [cost, next_hop, port]
        self.distance_vector[addr] = cost
        self.neighbours[addr] = port
        #lets send this distance vector to neighbours
        self.broadcast_to_neighbours()        
        #what if the node already exists
        


    def handleRemoveLink(self, port):
        """TODO: handle removed link"""
        # update the distance vector of this router
        # update the forwarding table
        # broadcast the distance vector of this router to neighbors
        addr = ""
        # print("removing link at port:", port)
        for dests in self.neighbours:
            if self.neighbours[dests] == port:
                addr = dests
        if addr != "":
            # print("address is:", addr)
            self.forwarding_table[addr] = [16,0,0]
            self.distance_vector[addr] = 16
            del self.neighbours[addr]
            for dests in self.forwarding_table:
                if self.forwarding_table[dests][1] == addr:
                    self.forwarding_table[dests] = [16, 0, 0]
                    self.distance_vector[dests] = 16
            # self.printer()
            
            #lets send this distance vector to neighbours
            self.broadcast_to_neighbours() 


    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        if timeMillisecs - self.last_time >= self.heartbeatTime:
            self.last_time = timeMillisecs
            # broadcast the distance vector of this router to neighbors
            self.broadcast_to_neighbours()


    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return "hello"

    def printer(self):
        print("my neighbours:", self.neighbours)
        print("my distance_vector:", self.distance_vector)
        print("my ftable:", self.forwarding_table)
