cmake_minimum_required(VERSION 2.8.3)

project(multimaster)

set(BUILD_DEPS
  rosgraph
  rospy
  roslib)

set(RUNTIME_DEPS
  rosgraph
  rospy
  roslib)

### Catkin ###
find_package(catkin REQUIRED COMPONENTS ${BUILD_DEPS})
catkin_package(CATKIN_DEPENDS ${RUNTIME_DEPS}
  LIBRARIES ${PROJECT_NAME})

### Install Launch Files ###
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch)

### Install Python Scripts ###
catkin_install_python(PROGRAMS scripts/master_sync.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
