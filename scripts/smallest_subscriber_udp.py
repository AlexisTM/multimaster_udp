#!/usr/bin/env python
import rospy

from multimaster_udp.transport import BroadcastSubscriber
from std_msgs.msg import String

def callback(data, topic):
    global counter
    counter += 1
    print data, "\n received",counter, "UDP messages from \n", topic

def main():
    global counter
    counter = 0
    rospy.init_node("smallest_subscriber_udp")
    # if the callback is not defined (None), it will publish locally 
    # to the equivalent topic.
    sub = BroadcastSubscriber("hello", String, callback=None)
    rospy.spin()

if __name__ == '__main__':
    main()