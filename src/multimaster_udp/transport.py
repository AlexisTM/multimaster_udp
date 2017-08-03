#!/usr/bin/env python
# https://stackoverflow.com/questions/12607516/python-udp-broadcast-not-sending
# https://stackoverflow.com/questions/15962119/using-bytearray-with-socket-recv-into
from socket import *

import sys
import threading

import rospy
from StringIO import StringIO

from multimaster_udp.dynamic_load import get_class

from multimaster_udp.msg import Msg, TopicInfo
from multimaster_udp.srv import AdvertiseUDP

if sys.version_info >= (3, 0): import socketserver
else: import SocketServer as socketserver 

def UDPSetup(topic_name, data_type, port=None):
    if port is None:
        topic = TopicInfo(topic_name, data_type._type, data_type._md5sum, 0)
        rospy.wait_for_service("organizer/topic")
        topic_srv = rospy.ServiceProxy("organizer/topic", AdvertiseUDP)
        result = topic_srv.call(topic)
        return result.topic
    else:
        return TopicInfo(topic_name, data_type._type, data_type._md5sum, port)

class BroadcastPublisher(object):
    """docstring for BroadcastPublisher"""
    def __init__(self, topic_name, data_type, network_address="192.168.1.1", network_size=8, port=None):
        super(BroadcastPublisher, self).__init__()
        self.n_sent = 0
        self.topic = UDPSetup(topic_name, data_type, port)
        self.setup_communications()

        self.network = self.__make_address(network_address, network_size, self.topic.port)
        # Use ready once communication to the master is done, also, update the port
        self.ready = True

    def setup_communications(self):
        self.cs = socket(AF_INET, SOCK_DGRAM)
        self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def __send(self, data):
        if data._type == "multimaster_udp/Msg":
            buff = StringIO()
            data.serialize(buff)
            self.cs.sendto(buff.getvalue(), self.network)
        else: pass # Wrong msg type

    def publish(self, rosmsg):
        """
        publish(rosmsg)

        High level publish of messages
        """
        if self.ready:
            msg = Msg()
            if self.topic.data_type != rosmsg._type:
                return # Fail, wrong message type
            buff = StringIO()
            rosmsg.serialize(buff)
            msg.data = buff.getvalue()
            self.__send(msg)

    def __make_address(self, network_address, network_size, port):
        """ __make_address creates a network 
        adress and returns it in the str format

        192.168.1.12/8 returns 192.168.1.255 
        """
        splitted = map(int, network_address.split('.'))
        current = 3
        while network_size > 0 and current >= 0:
            if network_size >= 8:
                splitted[current] = 255
            else :
                splitted[current] = splitted[current] | (2**network_size-1)
            network_size -= 8
            current -= 1
        return (".".join(map(str, splitted)), port)

class UDPHandlerServer(socketserver.UDPServer):
    """docstring for UDPHandlerServer"""
    # IP limitation
    max_packet_size = 64000
    allow_reuse_address = True

    def __init__(self, callback, *args, **kwargs):
        socketserver.UDPServer.__init__(self, *args, **kwargs)
        self.callback = callback

    def finish_request(self, request, client_address):
        self.callback(request, client_address)

class BroadcastSubscriber(object):
    """docstring for BroadcastSubscriber"""
    def __init__(self, topic_name, data_type, callback=None, port=None):

        self.data_type = data_type
        self.topic = UDPSetup(topic_name, data_type, port)

        if callback is None:
            self.local_pub = rospy.Publisher(topic_name, data_type, queue_size=10)
        else: 
            self.callback = callback

        self.server = UDPHandlerServer(self.__handle_callback, ("0.0.0.0", self.topic.port), socketserver.BaseRequestHandler)
        self.t = threading.Thread(target = self.server.serve_forever)
        self.t.start()

        rospy.on_shutdown(self.shutdown)

    def __handle_callback(self, request, client_address):
        inmsg = Msg()
        inmsg.deserialize(request[0])
        if inmsg.status & Msg.IS_FRAGMENT:
            pass  # Save data to later deserialization
        else: 
            msg = self.data_type()
            msg.deserialize(inmsg.data)
            self.callback(msg, self.topic)

    def callback(self, msg, topic):
        self.local_pub.publish(msg)

    def shutdown(self):
        self.server.shutdown()
