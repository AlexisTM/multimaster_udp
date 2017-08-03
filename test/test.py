#!/usr/bin/env python
import rospy

from multimaster_udp.transport import BroadcastPublisher6
from std_msgs.msg import String

import loremipsum

def main():
    rospy.init_node("smallest_broadcast_publisher_udp")

    pub = BroadcastPublisher6("hello", String)
    
    print pub.topic.port
    # max_size = 66000
    # string = ""
    # for i in xrange(max_size):
    #     if not i % 100:
    #         print max_size-i
    #     try:
    #         string = "".join(["W"]*(max_size-i))
    #         msg = String(string)
    #         #pub.publish(msg)
    #         print len(string)
    #         return
    #     except:
    #         pass
    #         
    #         
    r = rospy.Rate(25)
    divider = 1000
    max_size = 100000/divider
    min_size = 17000/divider
    string = ""
    for i in xrange(min_size,max_size):
        i = i*divider
        if not i % 1000:
            print i
        if rospy.is_shutdown(): return
        try:
            string = "".join(["W"]*(i))
            msg = String(string)
            pub.publish(msg)
            #print len(string)
            r.sleep()
            #return
        except:
            print "FAIL", len(string)
            return
            pass

    #pub.publish(String("".join(["W"]*400)))

    #print len(string)
if __name__ == '__main__':
    main()
