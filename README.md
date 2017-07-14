# multimaster_udp

Multimaster is a originally fork of the original repo on bitbucket (multimaster) from daenny. Now it focuses on getting UDP broadcast then UDP multicast message passing.

# UDP broadcast

### Architecture

* One port for each topic/data_type
* Ports chosen are the default port (11411) +1 for each pair (topic/data_type) 
* Robots (Subscribers/Publishers) calls the service `organizer/topic` with a `multimaster_udp/AdvertiseUDP` message to get the port number
* The `multimaster_udp/AdvertiseUDP` message consist of a `multimaster_udp/TopicInfo` message you have to fill in, omitting the port, the answer from the `organizer.py` will be the `multimaster_udp/TopicInfo` message with the port filled in.


### Test the current status

Build the repo, then execute:

```
roscore &
rosrun multimaster_udp client_udp.py

# in another terminal
roscd multimaster_udp
cd src/multimaster_udp
./transport.py
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
