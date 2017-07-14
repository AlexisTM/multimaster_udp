#!/usr/bin/env python
import rospy

from multimaster_udp.transport import UDPBroadcastPub, UDPBroadcastSub
from std_msgs.msg import String

def main():
    rospy.init_node("smallest_server_udp")

    msg = String("World")
    pub = UDPBroadcastPub("hello", String)
    
    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    main()