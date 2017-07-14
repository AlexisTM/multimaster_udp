# multimaster_udp

Multimaster is a originally fork of the original repo on bitbucket (multimaster) from daenny. Now it focuses on getting UDP broadcast then UDP multicast message passing.

# UDP broadcast

### Architecture

* One port for each topic/data_type
* Ports chosen are the default port (11411) +1 for each pair (topic/data_type) 
* Robots (Subscribers/Publishers) calls the service `organizer/topic` with a `multimaster_udp/AdvertiseUDP` message to get the port number
* The `multimaster_udp/AdvertiseUDP` message consist of a `multimaster_udp/TopicInfo` message you have to fill in, omitting the port, the answer from the `organizer.py` will be the `multimaster_udp/TopicInfo` message with the port filled in.

### USAGE

***Smallest UDP subscriber***

```python
#!/usr/bin/env python
import rospy

from multimaster_udp.transport import UDPBroadcastSub
from std_msgs.msg import String

def callback(data, topic):
    global counter
    counter += 1
    print data, "\n received",counter, "UDP messages from \n", topic

def main():
    global counter
    counter = 0
    rospy.init_node("smallest_client_udp")
    # publish to the /hello topic
    sub = UDPBroadcastSub("hello", String, callback=None)
    # sub = UDPBroadcastSub("hello", String, callback=callback)
    sub.spin()

if __name__ == '__main__':
    main()
```

***Smallest UDP publisher***

```python
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
```



### Test the current status

Build the repo, then execute:

```
roscore &
rosrun multimaster_udp organizer.py

# in another terminal
rosrun multimaster_udp smallest_client_udp.py
# in another terminal
rosrun multimaster_udp smallest_server_udp.py
```


# master_sync 
Original library 

### Usage

Yaml configuration file

```
local_pubs: [local_topics_to_register_at_foreign_master]
foreign_pubs: [foreign_topics_to_register_at_local_master]
local_services: [local_services_to_register_at_foreigner]
foreign_services: [foreign_services_to_register_at_local]
```

### Example

The local master is running a turtle which publish its position and state while using a service to set the destination to travel to.
  
* topics : 
    * /turtle0/position
    * /turtle0/state
* services:
    * /turtle0/setGoal

The foreign master is managing the turtle(s), publishing the map. It wants to call the turtle0 service.

* /master/map

The master_sync.py node will be ran onto the turtle computer and the configuration for this example is:

```
local_pubs: ["/turtle0/position", "/turtle0/state"]
foreign_pubs: ["/master/map"]
local_services: ["/turtle0/setGoal"]
foreign_services: []
```

# Credits

- Alexis Paques (@AlexisTM)
- daenny
