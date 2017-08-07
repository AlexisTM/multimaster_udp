#!/usr/bin/env python
import rospy

from multimaster_udp.transport import BroadcastPublisher6
from std_msgs.msg import String


def main():
    rospy.init_node("smallest_broadcast_publisher_udp")

    msg = String("World")
    pub = BroadcastPublisher6("hello", String)

    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    main()
