#! /usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		Hologlyph Bots (HB) Theme (eYRC 2023-24)
*        		===============================================
*
*  This script is to implement Task 2A of Hologlyph Bots (HB) Theme (eYRC 2023-24).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''
# Team ID:		1282
# Author List:	Akshar Dash, Rohan Mohapatra
# Filename:		feedback.py
# Functions:
#			[ ]
# Nodes:		Publshing nodes:
#              Subscribing nodes:    
# Import necessary libraries and modules
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose2D
import cv2
from cv_bridge import CvBridge
import numpy as np
import math

# Initialize some variables
mid_x = 0
mid_y = 0
a = 0
img_const = 1.5  # Image scaling constant

# Define a class for the ArUco marker detection node
class ArUcoDetector(Node):

    def __init__(self):
        super().__init__('ar_uco_detector')
        # Create subscriptions and publishers for the ArUco markers and images
        self.sub = self.create_subscription(Image, "/camera/image_raw", self.image_callback, 10)
        self.pub_1 = self.create_publisher(Pose2D, '/detected_aruco_1', 10)
        self.pub_2 = self.create_publisher(Pose2D, '/detected_aruco_2', 10)
        self.pub_3 = self.create_publisher(Pose2D, '/detected_aruco_3', 10)
        self.cvimg = CvBridge()

    # Callback function for processing images
    def image_callback(self, msg):
        global a, ids, corners
        # Convert ROS image message to an OpenCV image
        self.cv_image_1 = self.cvimg.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.cv_image = self.cv_image_1[13:487, 13:487]  # Crop the image

        height, width = self.cv_image.shape[:2]
        self.zoomed_image = cv2.resize(self.cv_image, (1000, 1000))  # Resize the image
        self.test_image = cv2.resize(self.cv_image, (1000, 1000))  # Create a copy of the image for testing

        # Detect ArUco markers in the image
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        parameters = cv2.aruco.DetectorParameters()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(self.zoomed_image, aruco_dict, parameters=parameters)

        # Draw detected ArUco markers on the test image
        if corners:
            for id, corn in zip(ids, corners):
                cv2.polylines(self.test_image, [corn.astype(np.int32)], True, (255, 0, 0), 2, cv2.LINE_AA)

        # Show the test image with detected markers
        cv2.imshow("frame", self.test_image)
        cv2.waitKey(1)

        # Process the detected markers and publish their Pose2D information
        self.req_list = []
        self.bot_1_info = []
        self.bot_2_info = []
        self.bot_3_info = []
        if ids is not None:
            for i, aruco_id in enumerate(ids):
                self.req_x = float(corners[i][0][:, 0].mean())
                self.req_y = float(corners[i][0][:, 1].mean())
                self.req_list.append([aruco_id, self.req_x, self.req_y])

        try:
            # Extract and process Pose2D information for each detected marker
            for i in range(0, len(self.req_list)):
                if self.req_list[i][0] == [1]:
                    self.bot_1_info = self.req_list[i]
                if self.req_list[i][0] == [2]:
                    self.bot_2_info = self.req_list[i]
                if self.req_list[i][0] == [3]:
                    self.bot_3_info = self.req_list[i]

            # Calculate Pose2D information for each ArUco marker
            corner_list_1 = cor(self.bot_1_info[0][0])
            z_axis_1 = yaw(corner_list_1, self.bot_1_info)
            self.pose_msg_bot1 = Pose2D()
            self.pose_msg_bot1.x = (self.bot_1_info[1]) / 2
            self.pose_msg_bot1.y = ((self.bot_1_info[2] - 1000) * (-1)) / 2
            self.pose_msg_bot1.theta = z_axis_1

            corner_list_2 = cor(self.bot_2_info[0][0])
            z_axis_2 = yaw(corner_list_2, self.bot_2_info)
            self.pose_msg_bot2 = Pose2D()
            self.pose_msg_bot2.x = (self.bot_2_info[1]) / 2
            self.pose_msg_bot2.y = ((self.bot_2_info[2] - 1000) * (-1)) / 2
            self.pose_msg_bot2.theta = z_axis_2

            corner_list_3 = cor(self.bot_3_info[0][0])
            z_axis_3 = yaw(corner_list_3, self.bot_3_info)
            self.pose_msg_bot3 = Pose2D()
            self.pose_msg_bot3.x = (self.bot_3_info[1]) / 2
            self.pose_msg_bot3.y = ((self.bot_3_info[2] - 1000) * (-1)) / 2
            self.pose_msg_bot3.theta = z_axis_3

            # Publish Pose2D information for each marker
            self.pub_1.publish(self.pose_msg_bot1)
            self.pub_2.publish(self.pose_msg_bot2)
            self.pub_3.publish(self.pose_msg_bot3)

            # Log the Pose2D information
            self.get_logger().info(f'{self.pose_msg_bot1}')
            self.get_logger().info(f'{self.pose_msg_bot2}')
            self.get_logger().info(f'{self.pose_msg_bot3}')
        except:
            # Handle exceptions if any occur
            self.get_logger().info('Oops...')

# Function to extract corner coordinates of a specific ArUco marker
def cor(desired_id):
    cor_list = []
    if ids is not None and desired_id in ids:
        desired_index = np.where(ids == desired_id)[0]  # Extract the integer index
        if desired_index.size > 0:
            # Access and work with the corners of the specific ArUco marker
            desired_corners = corners[desired_index[0]]
            for marker_corners in desired_corners:
                for corner in marker_corners:
                    x, y = corner
                    cor_list.append([x, y])
    return cor_list

# Function to calculate the yaw angle based on corner coordinates and marker information
def yaw(corner_list, bot_info):
    global mid_x, mid_y
    try:
        mid_x = (corner_list[1][0] + corner_list[2][0]) / 2
        mid_y = (corner_list[1][1] + corner_list[2][1]) / 2
    except:
        pass
    x = mid_x - bot_info[1]
    y = mid_y - bot_info[2]
    return math.atan2(-y, x)

# Main function to initialize the ROS node and start


def main(args=None):
    rclpy.init(args=args)

    aruco_detector = ArUcoDetector()

    rclpy.spin(aruco_detector)

    aruco_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()