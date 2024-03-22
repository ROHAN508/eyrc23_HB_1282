# ```
# * Team Id : HB#1282
# * Author List : AKSHAR DASH, ROHAN MOHAPATRA
# * Filename: feedback
# * Theme: HologlyphBots
# * Functions: get_yaw,cor
# * Global Variables: corner_ids,bot_ids,i,a,framed,frame,prev_positions,mid_x,mid_y
###########################






import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose2D
import cv2
from cv_bridge import CvBridge
import numpy as np
import math
corner_ids=[8,10,12,4]##stores the corner aruco ids of the arena
# corner_ids=[4,12,10,8]
bot_ids=[1,2,3] ##stores the ids of the bots
arena_corlist=[] ## variable initialisation to store the corners of aruco ids at the arena
i=0##index for corner list
a=0##checks wheather the perspective transform has occured or not
framed=0## checks if the image feed is framed or not
frame=[]##stores the corners of the arena
prev_positions = {'1': [], '2': [], '3': []}##  stores previous positions of the bots in order to draw the illustration lines
mid_x=0
mid_y=0
# Declare points_in_last_20_frames as a global variable
points_in_last_20_frames = {'1': [], '2': [], '3': []}

##node of camera feed
class ArUcoDetector(Node):

    def __init__(self):
        super().__init__('feedback_node')
        self.buffer=10
        ##necessary subscriptions and publishers are created for the bots
        self.sub = self.create_subscription(Image, "/camera1/image_raw", self.image_callback, self.buffer)
        self.pen1= self.create_publisher(Pose2D,"/pen1_pose",self.buffer)
        self.pen2= self.create_publisher(Pose2D,"/pen2_pose",self.buffer)
        self.pen3= self.create_publisher(Pose2D,"/pen3_pose",self.buffer)
        self.pen1_pos= Pose2D()
        self.pen2_pos= Pose2D()
        self.pen3_pos= Pose2D()

        self.cvimg = CvBridge()
        # Camera calibration parameters
        self.camera_matrix = np.array([[419.71324, 0., 324.18661],
                                       [0., 424.36412, 262.8046],
                                       [0., 0., 1.]])

        self.distortion_coefficients = np.array([-0.355877, 0.106938, -0.011005, 0.004376, 0.000000])

    ##callback for image feed from /camera_raw topic
    def image_callback(self, msg):
        global a, ids, corners,framed,i,a,prev_positions
        try:
            self.cv_image = self.cvimg.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error('Error converting ROS Image to OpenCV image: %s' % str(e))
            return
        
        ##the image is first undistored and then it is scaled 2X
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
        
        # cv2.imshow('undis',self.undistorted_image)
        # cv2.waitKey(1) 
        ## if the coner list is empty, the ids and corners of the ids are appended to the corner list
        if cor(corner_ids[i])!=[]:
            if len(arena_corlist)!=4:
                arena_corlist.append([corner_ids[i],cor(corner_ids[i])])
                
                if i<3:
                    i+=1
                ##a is set to 1 which means that the arena corners coordinates have been recorded    
                else:
                    a=1
                        
        if a==1:
            ##after finding the corners of the markers , the corners of intrest are extracted and then framed is set to 1
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

                ##the detected arucos have a red outline around them due to this part
                if corners1:
                    for id, corn in zip(ids1, corners1):
                        cv2.polylines(self.transformed_image, [corn.astype(np.int32)], True, (0, 0, 255), 2, cv2.LINE_AA) 
                
                if ids1 is not None:
                    ##initialisation of the list of the centres of bot aruco markers    
                    self.centroids = []
                    for j, aruco_id1 in enumerate(ids1):
                        ##if the detected ids match with the bot aruco ids they are appended to a list with centriod and id
                        if aruco_id1[0] in [1, 2, 3]:
                            centroid_x = int(corners1[j][0][:, 0].mean())
                            centroid_y = int(corners1[j][0][:, 1].mean())
                            
                            yaw = self.get_yaw(centroid_x,centroid_y, corners1[j][0])
                            
                            self.centroids.append([aruco_id1[0], centroid_x, centroid_y,yaw])
                            points_in_last_20_frames[str(aruco_id1[0])].append((centroid_x, centroid_y))
                            ##debugging logger
                            self.get_logger().info(f'YAW:  {aruco_id1[0],yaw}')
                            ## pose of detected aruco ids being stored in the respective attributes
                            if aruco_id1[0]==1:
                                
                                self.pen1_pos.x=(float(centroid_x))
                                
                                # self.pen1_pos.y=((float(centroid_y)-500)*-1)
                                self.pen1_pos.y=((float(centroid_y)))
                                self.pen1_pos.theta=float(yaw)
                                self.get_logger().info(f'{self.pen1_pos}')
                                self.pen1.publish(self.pen1_pos)


                            if aruco_id1[0]==2:
                                self.pen2_pos.x=float(centroid_x)
                                # self.pen2_pos.y=(float(centroid_y)-500)*-1
                                self.pen2_pos.y=((float(centroid_y)))
                                self.pen2_pos.theta=float(yaw)
                                self.pen2.publish(self.pen2_pos)

                            if aruco_id1[0]==3:
                                self.pen3_pos.x=float(centroid_x)
                                # self.pen3_pos.y=(float(centroid_y)-500)*-1
                                self.pen3_pos.y=((float(centroid_y)))
                                self.pen3_pos.theta=float(yaw)
                                self.pen3.publish(self.pen3_pos)
                            ##visualisation of trajectory of the bots
                            if len(points_in_last_20_frames[str(aruco_id1[0])]) > 500:
                                points_in_last_20_frames[str(aruco_id1[0])].pop(0)

                            # Draw trajectory
                            for point in points_in_last_20_frames[str(aruco_id1[0])]:
                                cv2.circle(self.transformed_image, point, 2, (0, 255, 0), -1)

                            # Update previous positions
                            prev_positions[str(aruco_id1[0])] = [centroid_x, centroid_y]

                
                # self.get_logger().info(f'Centroid Coordinates: {self.centroids}')
                ## to show the perspective transformed image
                cv2.imshow('Transformed Image', self.transformed_image)
                cv2.waitKey(1)   
        else:
            ##debugging logger in order to prompt the user to put the arena in frame or remove any object blocking the camera view
            self.get_logger().info('pls put the arena in frame')




# ``
# * Function Name: get_yaw
# * Input: self, the centriod x and centroid y coordinate
# * Output: yaw of the aruco id
# * Logic: it measures the angle that the line joining the centre of the right side of the aruco marker and the
            #centroid of the aruco marker makes with the global x axis
# * in the function>
# * Example Call: get_yaw(self,centroid_x,centroid_y,corner_list)                
    def get_yaw(self,centroid_x,centroid_y,corner_list):
        
        global mid_x, mid_y
        try:
            mid_x = (corner_list[1][0] + corner_list[2][0]) / 2
            mid_y = (corner_list[1][1] + corner_list[2][1]) / 2
        except:
            pass
        x = mid_x - centroid_x
        y = mid_y - centroid_y
        return math.atan2(-y, x)

    # Return None if the specified ArUco marker is not found
        # return None         

        
        
            
            
                
            

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