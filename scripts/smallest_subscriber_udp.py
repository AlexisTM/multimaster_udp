#!/usr/bin/env python
import rospy

from multimaster_udp.transport import BroadcastSubscriber6
from std_msgs.msg import String


def callback(data, topic):
    global counter
    counter += 1
    print "\n received", counter, "UDP messages from \n", topic, "len(data)= ", len(data.data)


def main():
    global counter
    counter = 0
    rospy.init_node("smallest_subscriber_udp", anonymous=True)
    # if the callback is not defined (None), it will publish locally
    # to the equivalent topic.
    sub = BroadcastSubscriber6("hello", String, callback=callback)

    print sub.topic.port
    rospy.spin()

if __name__ == '__main__':
    main()
