#!/usr/bin/env python
# https://stackoverflow.com/questions/12607516/python-udp-broadcast-not-sending
# https://stackoverflow.com/questions/15962119/using-bytearray-with-socket-recv-into
from socket import *

from rospy.msg import AnyMsg

class UDPMulticast(object):
    """docstring for UDPMulticast"""
    def __init__(self, arg):
        super(UDPMulticast, self).__init__()
        self.arg = arg


class UDPBroadcastPub(object):
    """docstring for UDPBroadcastPub"""
    def __init__(self, port=11411, network_address="192.168.1.1", network_size=8):
        super(UDPBroadcastPub, self).__init__()
        self.network = self.makeAddress(network_address, network_size, port)

        self.cs = socket(AF_INET, SOCK_DGRAM)
        self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.ready = True

    def send(self, data):
        self.cs.sendto(data, self.network)

    def makeAddress(self, network_address, network_size, port):
        splitted = map(int, network_address.split('.'))
        current = 0
        while network_size > 0 and current < 4:
            if network_size >= 8:
                splitted[current] = 255
            else :
                splitted[current] = splitted[current] | (2**network_size-1)
            network_size -= 8
        return (".".join(map(str, splitted)), port)

class UDPBroadcastSub(object):
    """docstring for UDPBroadcastSub"""
    topics = {}
    def __init__(self, port=11411):
        super(UDPBroadcastSub, self).__init__()
        self.port = port

        self.cs = socket(AF_INET, SOCK_DGRAM)
        self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.cs.bind(('', self.port))

    def spin(self):
        a = bytearray()
        buff = memoryview(a)
        print self.cs.recvfrom_into(buff)
        self.callback(a)

    def callback(self, a):
        print a

def test():
    a = UDPBroadcastPub()
    a.send("hey")

if __name__ == '__main__':
    test()


        