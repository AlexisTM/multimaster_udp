#!/usr/bin/env python
# https://stackoverflow.com/questions/12607516/python-udp-broadcast-not-sending
# https://stackoverflow.com/questions/15962119/using-bytearray-with-socket-recv-into
from socket import *

# Dynamic load msg classes
import roslib
import imp
import sys

import threading

import rospy
from StringIO import StringIO

from multimaster_udp.msg import Msg, TopicInfo
from multimaster_udp.srv import AdvertiseUDP

if sys.version_info >= (3, 0):
    import socketserver
else:
    import SocketServer as socketserver 

def get_class(msg_class):
    def load_pkg_module(package, directory):
        #check if its in the python path
        path = sys.path
        try:
            imp.find_module(package)
        except:
            roslib.load_manifest(package)
        try:
            m = __import__( package + '.' + directory )
        except:
            rospy.logerr( "Cannot import package : %s"% package )
            rospy.logerr( "sys.path was " + str(path) )
            return None
        return m

    def load_message(package, message):
        m = load_pkg_module(package, 'msg')
        m2 = getattr(m, 'msg')
        return getattr(m2, message)

    try:
        loaded_class = load_message(*msg_class.split('/'))
    except:
        loaded_class = None
    finally:
        return loaded_class

def UDPSetup(topic_name, data_type):
    topic = TopicInfo(topic_name, data_type._type, data_type._md5sum, 0)
    rospy.wait_for_service("organizer/topic")
    topic_srv = rospy.ServiceProxy("organizer/topic", AdvertiseUDP)
    result = topic_srv.call(topic)
    return result.topic

class UDPPublisher(object):
    """docstring for UDPPublisher"""
    def __init__(self, topic_name, data_type, network_address="192.168.1.1", network_size=8):
        super(UDPPublisher, self).__init__()

        self.topic = UDPSetup(topic_name, data_type)
        port = self.setup_communications()

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
        else: 
            # Wrong msg type
            pass

    def publish(self, rosmsg):
        """
        publish(rosmsg)

        High level publish of messages
        """
        if self.ready:
            msg = Msg()
            msg.data_type = rosmsg._type
            buff = StringIO()
            rosmsg.serialize(buff)
            msg.data = buff.getvalue()
            msg.length = buff.len
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

class UDPSubscriber(object):
    """docstring for UDPSubscriber"""
    def __init__(self, topic_name, data_type, callback=None):
        self.data_type = data_type
        self.topic = UDPSetup(topic_name, data_type)

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
        if inmsg.data_type == self.topic.data_type:
            msg = self.data_type()
            msg.deserialize(inmsg.data)
            self.callback(msg, self.topic)

        # else error or 
        # Dynamic message loading
        # dataClass = get_class(inmsg.data_type)
        # msg = dataClass()

    def callback(self, msg, topic):
        self.local_pub.publish(msg)

    def shutdown(self):
        self.server.shutdown()
