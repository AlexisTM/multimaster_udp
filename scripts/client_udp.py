#!/usr/bin/env python

import rospy

from multimaster_udp.transport import UDPBroadcastPub, UDPBroadcastSub
from multimaster_udp.msg import TopicInfo
from std_msgs.msg import String

from multimaster_udp.srv import AdvertiseUDP

class UDPBroadcastClient(object):
    """docstring for UDPBroadcastClient"""
    def __init__(self, arg):
        super(UDPBroadcastClient, self).__init__()

        self.arg = arg

def main():
    rospy.init_node("client_udp")

    rospy.wait_for_service("/organizer/topic")
    udp_topic_srv = rospy.ServiceProxy("/organizer/topic", AdvertiseUDP)

    topic = TopicInfo()
    topic.topic_name = "/hey/i/use/udp"
    topic.data_type = String._type
    topic.md5sum = String._md5sum
    result = udp_topic_srv.call(topic)
    topic = result.topic

    sub = UDPBroadcastSub()
    sub.spin()

    #UDPBroadcastSub()

if __name__ == '__main__':
    main()