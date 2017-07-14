#!/usr/bin/env python


import rospy

from multimaster_udp.msg import TopicInfoArray
from multimaster_udp.srv import AdvertiseUDP

class Organizer(object):
    """docstring for Organizer

    Topics holds all the topics broadcasted
    Maintain the lookup table and the raw topics to send

    topics: topics is a multimaster_udp/TopicInfoArray msg.
    topics = [{name: "/topic",
              port: 11411,
              data_type: "std_msgs/String",
              md5sum: "135e135e135e135e135e135e135e135e"}]
    
    Lookup table: {topic_name: [port]}
    """
    INITIAL_UDP_PORT = 11411

    lookup = {}
    topics = TopicInfoArray()

    def __init__(self):
        super(Organizer, self).__init__()
        rospy.Service("organizer/topic", AdvertiseUDP, self.__advertise_callback)
        #self.udptopics_pub = rospy.Publisher("organizer/udptopics", TopicInfoArray, queue_size=1)
        #self.topics.topics = []

    def __advertise_callback(self, srv_msg):
        result = self.add(srv_msg.topic)
        return result

    def add(self, topic):
        topic = self.set_port(topic)
        return (True, "Success", topic)

    def set_port(self, topic):
        h = hash(topic.topic_name + topic.data_type)
        if not self.lookup.__contains__(h):
            topic.port = self.INITIAL_UDP_PORT + len(self.lookup)
            self.lookup[h] = topic
            self.topics.topics.append(topic)
            return topic
        else:
            return self.lookup[h]

    def spin(self):
        rate = rospy.Rate(0.1)
        rospy.spin()
        #while not rospy.is_shutdown():
        #    self.udptopics_pub.publish(self.topics)
        #    rate.sleep()

def main():
    organizer = Organizer()
    organizer.spin()

if __name__ == '__main__':
    rospy.init_node("app_organizer_server")
    main()