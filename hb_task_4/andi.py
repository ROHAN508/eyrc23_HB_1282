import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose2D
import cv2
from cv_bridge import CvBridge
import numpy as np
import math
corner_ids=[8,10,12,4]
bot_ids=[1,2,3]
arena_corlist=[]
i=0
a=0
framed=0
frame=[]

class ArUcoDetector(Node):

    def __init__(self):
        super().__init__('ar_uco_detector')
        self.sub = self.create_subscription(Image, "/camera1/image_raw", self.image_callback, 10)

        self.cvimg = CvBridge()
        # Camera calibration parameters
        self.camera_matrix = np.array([[419.71324, 0., 324.18661],
                                       [0., 424.36412, 262.8046],
                                       [0., 0., 1.]])

        self.distortion_coefficients = np.array([-0.355877, 0.106938, -0.011005, 0.004376, 0.000000])


    def image_callback(self, msg):
        global a, ids, corners,framed,i,a,k
        try:
            self.cv_image = self.cvimg.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error('Error converting ROS Image to OpenCV image: %s' % str(e))
            return
        
        
        self.test_img = cv2.undistort(self.cv_image, self.camera_matrix, self.distortion_coefficients)
        height, width = self.test_img.shape[:2]
        new_height = int(height * 2)
        new_width = int(width * 2)
        self.undistorted_image = cv2.resize(self.test_img, (new_width, new_height))


        # Detect ArUco markers
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        parameters = cv2.aruco.DetectorParameters()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(self.undistorted_image, aruco_dict, parameters=parameters)
            
        
        # if corners:
        #     for id, corn in zip(ids, corners):
        #         cv2.polylines(self.undistorted_image, [corn.astype(np.int32)], True, (0, 0, 255), 2, cv2.LINE_AA)
        
 
        if cor(corner_ids[i])!=[]:
            if len(arena_corlist)!=4:
                arena_corlist.append([corner_ids[i],cor(corner_ids[i])])
                
                if i<3:
                    i+=1
                else:
                    a=1    
        if a==1:
            if framed!=1:
                for i in range(0,4):
                    frame.append(arena_corlist[i][1][i])
                framed=1
            if len(frame) == 4:
                # Assuming 'frame' contains the four corner points of the region of interest
                pts1 = np.float32(frame)

                # Define the width and height of the rectangular region after transformation
                width, height = 500, 500  

                pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

                # Calculate the perspective transformation matrix
                matrix = cv2.getPerspectiveTransform(pts1, pts2)

                # Apply the perspective transformation to the image
                self.transformed_image = cv2.warpPerspective(self.undistorted_image, matrix, (width, height))
                
                  
                corners1, ids1, _ = cv2.aruco.detectMarkers(self.transformed_image,aruco_dict)
                if corners1:
                    for id, corn in zip(ids1, corners1):
                        cv2.polylines(self.transformed_image, [corn.astype(np.int32)], True, (0, 0, 255), 2, cv2.LINE_AA) 
                
                    
                self.centroids = []
                for j, aruco_id1 in enumerate(ids1):
                    if aruco_id1[0] in [1, 2, 3]:
                        centroid_x = int(corners1[j][0][:, 0].mean())
                        centroid_y = int(corners1[j][0][:, 1].mean())
                        self.centroids.append([aruco_id1[0], centroid_x, centroid_y])

                self.get_logger().info(f'Centroid Coordinates: {self.centroids}')

                cv2.imshow('Transformed Image', self.transformed_image)
                cv2.waitKey(1)   


                
    def get_aruco_yaw(self,aruco_id,corners,ids):
        # aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

        # corners, ids, _ = cv2.aruco.detectMarkers(self.undistorted_image,aruco_dict)

        if ids is not None and aruco_id in ids:
        # Find the index of the specified ArUco marker
            marker_index = np.where(ids == aruco_id)[0][0]

        # Extract the rotation vector for the specified marker
            rvecs, _, _ = cv2.aruco.estimatePoseSingleMarkers([corners[marker_index]], 1.0, self.camera_matrix, self.distortion_coefficients)

        # Extract the rotation matrix from the rotation vector
            rotation_matrix, _ = cv2.Rodrigues(rvecs[0])

        # Extract the yaw angle from the rotation matrix
            yaw_rad = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
            yaw_deg = np.degrees(yaw_rad)

            return yaw_deg

    # Return None if the specified ArUco marker is not found
        return None         

        
        
            
            
                
            
                    
        
      




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


def main(args=None):
    rclpy.init(args=args)
    output = ArUcoDetector()
    rclpy.spin(output)
    output.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()