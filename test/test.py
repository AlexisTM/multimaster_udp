#!/usr/bin/env python
import rospy

from multimaster_udp.transport import BroadcastPublisher
from std_msgs.msg import String

import loremipsum

def main():
    rospy.init_node("smallest_broadcast_publisher_udp")

    pub = BroadcastPublisher("hello", String)
    


    max_size = 66000
    string = ""
    for i in xrange(max_size):
        if not i % 100:
            print max_size-i
        try:
            string = "".join(["W"]*(max_size-i))
            msg = String(string)
            pub.publish(msg)
            print len(string)
            return
        except:
            pass



    pub.publish(String("".join(["W"]*65496)))
    pub.publish(String("".join(["W"]*65496)))
    pub.publish(String("".join(["W"]*65496)))
    pub.publish(String("".join(["W"]*65496)))
    pub.publish(String("".join(["W"]*65496)))

    print len(string)
if __name__ == '__main__':
    main()
