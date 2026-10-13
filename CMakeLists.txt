cmake_minimum_required(VERSION 3.0.2)
project(edge_detection_node)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  dynamic_reconfigure
  rospy
  sensor_msgs
)

generate_dynamic_reconfigure_options(cfg/Canny.cfg)

catkin_package(
  CATKIN_DEPENDS cv_bridge dynamic_reconfigure rospy sensor_msgs
)

catkin_install_python(PROGRAMS scripts/edge_detection.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
