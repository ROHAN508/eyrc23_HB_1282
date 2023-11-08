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
#! /usr/bin/env python3
# Team ID:		1282
# Author List:	Akshar Dash, Rohan Mohapatra
# Filename:		feedback.py
# Functions:
#			[ cor,yaw]
# Import necessary modules
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose2D
import cv2
from cv_bridge import CvBridge
import numpy as np
import math

# Initialize global variables
mid_x = 0
mid_y = 0
a = 0

# Initialize variables to store the centroid history


# Create a ROS 2 node for ArUco marker detection
class ArUcoDetector(Node):

    def __init__(self):
        super().__init__('ar_uco_detector')
        self.sub = self.create_subscription(Image, "/camera/image_raw", self.image_callback, 10)
        self.pub = self.create_publisher(Pose2D, '/detected_aruco', 10)
        self.cvimg = CvBridge()

    # Callback function to process camera image
    def image_callback(self, msg):
        global a, ids, corners,centroid_x,centroid_y
        self.cv_image = self.cvimg.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        height, width = self.cv_image.shape[:2]
        #resizing the image in order to properly detect all the markers.
        new_height = int(height * 1.5)
        new_width = int(width * 1.5)
        self.zoomed_image = cv2.resize(self.cv_image, (new_width, new_height))
        self.test_image = cv2.resize(self.cv_image, (new_width, new_height))

        # Detect ArUco markers
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        parameters = cv2.aruco.DetectorParameters()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(self.zoomed_image, aruco_dict, parameters=parameters)

        if corners:
            for id, corn in zip(ids, corners):
                cv2.polylines(self.test_image, [corn.astype(np.int32)], True, (0, 0, 255), 2, cv2.LINE_AA)
        
        cv2.imshow("frame", self.test_image)
        cv2.waitKey(1)


        self.req_list = []
        if ids is not None:
            for i, aruco_id in enumerate(ids):
                self.req_x = float(corners[i][0][:, 0].mean())
                self.req_y = float(corners[i][0][:, 1].mean())
                self.req_list.append([aruco_id, self.req_x, self.req_y])

        # Process ArUco marker positions
        if a == 0:
            self.req_list_1 = []
            self.dist_list = []
            for i in range(0, len(self.req_list)):
                for j in range(i + 1, len(self.req_list)):
                    self.dist = ((self.req_list[i][1] - self.req_list[j][1]) ** 2 +
                                 (self.req_list[i][2] - self.req_list[j][2]) ** 2) ** 0.5
                    self.req_list_1.append([self.req_list[i][0][0], self.req_list[j][0][0], self.dist])
                    self.dist_list.append(self.dist)
            #find the diagonal of the square and find all the corner aruco ids from calculated side length.
            self.max_dist = max(self.dist_list)
            self.error = self.max_dist * 0.01
            self.square_side = self.max_dist / ((2) ** 0.5)
            self.square_id = set()

            for i in range(0, len(self.req_list_1)):
                if self.req_list_1[i][2] < self.square_side + self.error and self.req_list_1[i][2] > self.square_side - self.error:
                    self.square_id.add(self.req_list_1[i][0])
                    self.square_id.add(self.req_list_1[i][1])
            self.square_id = list(self.square_id)
            self.x1 = 0
            self.y1 = 0
            self.bot_info = []

            for i in range(0, len(self.req_list)):
                if self.req_list[i][0] in self.square_id:
                    self.x1 = self.x1 + self.req_list[i][1]
                    self.y1 = self.y1 + self.req_list[i][2]
                else:
                    self.bot_info = self.req_list[i]

            # self.x1 = self.x1 / 4
            # self.y1 = self.y1 / 4
            a = 1

        for i in range(0, len(self.req_list)):
            if self.bot_info[0] == self.req_list[i][0]:
                self.bot_info[1] = self.req_list[i][1]
                self.bot_info[2] = self.req_list[i][2]

        corner_list = cor(self.bot_info[0][0])
        z_axis = yaw(corner_list, self.bot_info)

        self.pose_msg = Pose2D()
        #downsizing the coordinate as we had resized the original image to 1.5x 
        self.pose_msg.x = (self.bot_info[1]) / 1.5
        self.pose_msg.y = (((self.bot_info[2]) * (1) - 750) / 1.5) * (-1)
        self.pose_msg.theta = z_axis
        # Publish bot coordinates to the topic /detected_aruco
        self.pub.publish(self.pose_msg)
        self.get_logger().info(f'bot x : {self.pose_msg.x}')
        self.get_logger().info(f'bot y : {self.pose_msg.y}')
        self.get_logger().info(f'yaw : {z_axis}')

        

        

# Helper function to get corner coordinates of an ArUco marker
def cor(desired_id):
    cor_list = []
    if ids is not None and desired_id in ids:
        desired_index = np.where(ids == desired_id)[0]
        if desired_index.size > 0:
            desired_corners = corners[desired_index[0]]
            for marker_corners in desired_corners:
                for corner in marker_corners:
                    x, y = corner
                    cor_list.append([x, y])
    return cor_list

# Helper function to calculate the yaw of the bot
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

# Main function to initialize and run the ROS 2 node
def main(args=None):
    rclpy.init(args=args)
    aruco_detector = ArUcoDetector()
    rclpy.spin(aruco_detector)
    aruco_detector.destroy_node()
    rclpy.shutdown()
    


if __name__ == '__main__':
    main()
