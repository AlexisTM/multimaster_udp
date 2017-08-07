#!/usr/bin/env python
import rospy

from multimaster_udp.transport import BroadcastPublisher6
from std_msgs.msg import String

import loremipsum


def main():
    rospy.init_node("smallest_broadcast_publisher_udp")

    pub = BroadcastPublisher6("hello", String)

    print pub.topic.port
    r = rospy.Rate(10)
    divider = 100
    max_size = 100000/divider
    min_size = 1800/divider
    string = ""
    for i in xrange(min_size, max_size):
        i = i*divider
        if not i % 1000:
            print i
        if rospy.is_shutdown():
            return
        try:
            string = "".join(["W"]*(i))
            msg = String(string)
            pub.publish(msg)
            # print len(string)
            r.sleep()
            # return
        except:
            print "FAIL", len(string)
            return
            pass

    # print len(string)
if __name__ == '__main__':
    main()
