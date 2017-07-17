#!/usr/bin/env python
import rospy

from multimaster_udp.transport import UDPPublisher
from std_msgs.msg import String

def main():
    rospy.init_node("smallest_broadcast_publisher_udp")

    msg = String("World")
    pub = UDPPublisher("hello", String)

    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    main()
