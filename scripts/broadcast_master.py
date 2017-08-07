#!/usr/bin/env python


import rospy

from multimaster_udp.msg import TopicInfoArray, TopicInfo
from multimaster_udp.srv import AdvertiseUDP


class BroadcastMaster(object):
    """docstring for BroadcastMaster

    Topics holds all the topics broadcasted
    Maintain the lookup table and the raw topics to send

    topics: topics is a multimaster_udp/TopicInfoArray msg.
    topics = [{name: "/topic",
              port: 11411,
              data_type: "std_msgs/String",
              md5sum: "71f920fa275127a7b60fa4d4d41432a3"}]

    Lookup table: {hash(name,type,md5): port}
    """
    INITIAL_UDP_PORT = 11411

    lookup = {}
    topics = TopicInfoArray()

    def __init__(self):
        super(BroadcastMaster, self).__init__()
        rospy.Service("organizer/topic", AdvertiseUDP,
                      self.__advertise_callback)

    def __advertise_callback(self, srv_msg):
        result = self.add(srv_msg.topic)
        return result

    def add(self, topic):
        topic = self.set_port(topic)
        return (True, "Success", topic)

    def set_port(self, topic):
        h = hash(topic.name + topic.data_type + topic.md5sum)
        if not h in self.lookup:
            topic.port = self.INITIAL_UDP_PORT + len(self.lookup)
            self.lookup[h] = topic
            self.topics.topics.append(topic)
            return topic
        else:
            return self.lookup[h]


def main():
    organizer = BroadcastMaster()
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node("broadcast_master_py")
    main()
