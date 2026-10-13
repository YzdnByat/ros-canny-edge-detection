#!/usr/bin/env python3

import rospy
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from dynamic_reconfigure.server import Server
from edge_detection_node.cfg import CannyConfig


class CannyNode:
    def __init__(self):
        rospy.init_node("edge_detection_node")

        self.bridge = CvBridge()

        # Default params (will be overwritten by dynamic reconfigure callbacks)
        self.blur_ksize = 5
        self.th1 = 100
        self.th2 = 200

        # Publisher
        self.pub = rospy.Publisher(
            "/kitti/camera_color_left/canny_det",
            Image,
            queue_size=1
        )

        # Subscriber
        rospy.Subscriber(
            "/kitti/camera_color_left/image_raw",
            Image,
            self.callback,
            queue_size=1
        )

        # Dynamic reconfigure server
        self.server = Server(CannyConfig, self.reconfig_cb)

        rospy.loginfo("Canny node started with dynamic reconfigure.")

    def reconfig_cb(self, config, level):
        # Enforce odd blur kernel size
        k = int(config.blur_ksize)
        if k < 1:
            k = 1
        if k % 2 == 0:
            k += 1

        self.blur_ksize = k
        self.th1 = int(config.th1)
        self.th2 = int(config.th2)

        rospy.loginfo(f"Updated params: blur_ksize={self.blur_ksize}, th1={self.th1}, th2={self.th2}")
        return config

    def callback(self, msg):
        try:
            cv_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

            if self.blur_ksize > 1:
                gray = cv2.GaussianBlur(gray, (self.blur_ksize, self.blur_ksize), 0)

            edges = cv2.Canny(gray, self.th1, self.th2)

            out = self.bridge.cv2_to_imgmsg(edges, encoding="mono8")
            out.header = msg.header
            self.pub.publish(out)

        except Exception as e:
            rospy.logerr(e)


if __name__ == "__main__":
    node = CannyNode()
    rospy.spin()
