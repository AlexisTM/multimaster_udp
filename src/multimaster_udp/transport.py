#!/usr/bin/env python
# https://stackoverflow.com/questions/12607516/python-udp-broadcast-not-sending
# https://stackoverflow.com/questions/15962119/using-bytearray-with-socket-recv-into
from socket import *

# Dynamic load msg classes
import roslib
import imp
import sys

from StringIO import StringIO

from multimaster_udp.msg import Msg
from multimaster_udp.msg import TopicInfo
from rospy.msg import AnyMsg

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

class UDPMulticast(object):
    """docstring for UDPMulticast"""
    def __init__(self, arg):
        super(UDPMulticast, self).__init__()
        self.arg = arg

class UDPBroadcastPub(object):
    """docstring for UDPBroadcastPub"""
    def __init__(self, port=11411, network_address="192.168.1.1", network_size=8):
        super(UDPBroadcastPub, self).__init__()
        self.network = self.make_address(network_address, network_size, port)

        self.cs = socket(AF_INET, SOCK_DGRAM)
        self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        # Use ready once communication to the master is done, also, update the port
        self.ready = True

    def update_port(self, port):
        self.network = (self.network[0], port)

    def send(self, data):
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

            self.send(msg)

    def make_address(self, network_address, network_size, port):
        """ make_address creates a network 
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

class UDPBroadcastSub(object):
    """docstring for UDPBroadcastSub"""
    topics = {}
    def __init__(self, topic_name="", data_type="", port=11411, callback=None):
        super(UDPBroadcastSub, self).__init__()
        self.port = port
        self.data_type = data_type
        self.topic_name = topic_name
        self.cs = socket(AF_INET, SOCK_DGRAM)
        self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.cs.bind(('', self.port))
        self.callback = callback

    def spin(self):
        inmsg = Msg()
        buff = self.cs.recv(65000)
        inmsg.deserialize(buff)
        dataClass = get_class(inmsg.data_type)
        msg = dataClass()
        msg.deserialize(inmsg.data)
        if self.callback is None:
            pass
            #publish
        else :
            self.callback(msg, self.topic_name, self.data_type)

def test():
    a = UDPBroadcastPub()
    print a.network

    msg2 = TopicInfo()
    print "Sending TopicInfo"
    a.publish(msg2)

if __name__ == '__main__':
    test()


        