#!/usr/bin/env python
# https://stackoverflow.com/questions/12607516/python-udp-broadcast-not-sending
# https://stackoverflow.com/questions/15962119/using-bytearray-with-socket-recv-into

# Dynamic load msg classes
import roslib
import imp
import sys

import rospy
from StringIO import StringIO

from multimaster_udp.msg import Msg, TopicInfo
from multimaster_udp.srv import AdvertiseUDP

# SocketServer python2/3 compatibility
if sys.version_info >= (3, 0):
    import socketserver
else:
    import SocketServer as socketserver 

def UDPSetup(topic_name, data_type):
    topic = TopicInfo(topic_name, data_type._type, data_type._md5sum, 0)
    rospy.wait_for_service("organizer/topic")
    topic_srv = rospy.ServiceProxy("organizer/topic", AdvertiseUDP)
    result = topic_srv.call(topic)
    return result.topic



class UDPHandlerServer(socketserver.UDPServer):
    """docstring for UDPHandlerServer"""
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback

    def finish_request(self, request, client_address):
        inMsg = Msg()
        inmsg.deserialize(request[0])
        if inmsg.md5sum == self.data_type._md5sum :
            msg = self.data_type()
            msg.deserialize(inmsg.data)
            self.callback(msg, origin)

        # else error or 
        # Dynamic message loading
        # dataClass = get_class(inmsg.data_type)
        # msg = dataClass()


class UDPSubscriber(object):
    """docstring for UDPSubscriber"""
    def __init__(self, topic_name, data_type, callback=None):
        self.topic = UDPSetup(topic_name, data_type)

        if callback is None:
            self.local_pub = rospy.Publisher(topic_name, data_type, queue_size=10)
        else: 
            self.callback = callback

        self.server = socketserver.UDPServer(("0.0.0.0", self.topic.port), socketserver.BaseRequestHandler)
        # threadthis
        self.server.serve_forever()

    def callback(self, msg, topic):
        self.local_pub.publish(msg)
