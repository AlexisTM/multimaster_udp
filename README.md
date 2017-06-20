# multimaster

Multimaster is a fork of the original repo on bitbucket from daenny, to avoid to loose it.


# Usage

Yaml configuration file

```
local_pubs: [local_topics_to_register_at_foreign_master]
foreign_pubs: [foreign_topics_to_register_at_local_master]
local_services: [local_services_to_register_at_foreigner]
foreign_services: [foreign_services_to_register_at_local]
```

# Example

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
