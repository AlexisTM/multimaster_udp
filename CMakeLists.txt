cmake_minimum_required(VERSION 2.8.3)

project(multimaster_udp)

set(BUILD_DEPS
  rosgraph
  rospy
  roslib
  std_msgs
  message_generation)

set(RUNTIME_DEPS
  rosgraph
  rospy
  roslib
  message_runtime)

### Catkin ###
find_package(catkin REQUIRED COMPONENTS ${BUILD_DEPS})

catkin_python_setup()

add_message_files(
  FILES
  Msg.msg
  Fragment.msg
  TopicInfo.msg
  TopicInfoArray.msg
)

add_service_files(
  FILES
  AdvertiseUDP.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(CATKIN_DEPENDS ${RUNTIME_DEPS}
  LIBRARIES ${PROJECT_NAME})
    
### Install Launch Files ###
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch)

### Install Python Scripts ###
catkin_install_python(PROGRAMS scripts/master_sync.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
