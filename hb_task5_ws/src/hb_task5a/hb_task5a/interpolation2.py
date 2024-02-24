import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Wrench
from nav_msgs.msg import Odometry
import time
import math
import numpy as np
from std_msgs.msg import Bool
# from tf_transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from my_robot_interfaces.msg import Goal             
from std_msgs.msg import Float64MultiArray
import numpy as np
import matplotlib.pyplot as plt

rpmValues_right = [-47.62, -47.1, -43.165, -38.22, -31.91, -27.53, -22.47, -15.79, -10.53, 0.0, 0.0, 0.0, 0.0, 10.186, 14.32, 20.62, 26.2, 31.08, 36.81, 41.55, 47.17, 47.62, 47.62]
pwmValues_right =  [180, 170, 160, 150, 140, 130, 120, 110, 99, 96, 92, 90, 89, 88, 80, 70, 60, 50, 40, 30, 20, 10, 0]


rpmValues_left= [-48, -46.875, -42.735, -38.76, -32.36, -26.43, -21.81, -15.15, -9, 0.0, 0.0, 0.0, 0.0, 9.132, 12, 18.59, 24.21, 29.09, 35.087, 40.268, 44.313, 46.875, 46.875]
pwmValues_left= [180, 170, 160, 150, 140, 130, 120, 110, 97, 96, 92, 90, 88, 87, 80, 70, 60, 50, 40, 30, 20, 10, 0]

rpmValues_rear= [-45.429, -42.796, -37.735, -33.51, -29.126, -24.69, -20.134, -14.85, -9.933, 0.0, 0.0, 0.0, 0.0, 9.868, 12.97, 17.44, 20.97, 24.83, 29.91, 34.88, 39.47, 43.48, 45.45]
pwmValues_rear= [180, 170, 160, 150, 140, 130, 120, 110, 99, 96, 92, 90, 88, 87, 80, 70, 60, 50, 40, 30, 20, 10, 0]

##right
# Remove duplicate RPM values
unique_indices_right = np.unique(rpmValues_right, return_index=True)[1]
unique_indices_right = unique_indices_right[unique_indices_right < len(pwmValues_right)]
sorted_indices_right = np.argsort(np.array(rpmValues_right)[unique_indices_right])
sorted_rpm_right = np.array(rpmValues_right)[unique_indices_right][sorted_indices_right]
sorted_pwm_right = np.array(pwmValues_right)[unique_indices_right][sorted_indices_right]


##left
unique_indices_left = np.unique(rpmValues_left, return_index=True)[1]
unique_indices_left = unique_indices_left[unique_indices_left < len(pwmValues_left)]
sorted_indices_left = np.argsort(np.array(rpmValues_left)[unique_indices_left])
sorted_rpm_left = np.array(rpmValues_left)[unique_indices_left][sorted_indices_left]
sorted_pwm_left = np.array(pwmValues_left)[unique_indices_left][sorted_indices_left]

##rear
# Remove duplicate RPM values
unique_indices_rear = np.unique(rpmValues_rear, return_index=True)[1]
unique_indices_rear = unique_indices_rear[unique_indices_rear < len(pwmValues_rear)]
sorted_indices_rear = np.argsort(np.array(rpmValues_rear)[unique_indices_rear])
sorted_rpm_rear = np.array(rpmValues_rear)[unique_indices_rear][sorted_indices_rear]
sorted_pwm_rear = np.array(pwmValues_rear)[unique_indices_rear][sorted_indices_rear]






class interp(Node):
    def __init__(self):
        super().__init__('interpolator2')
        
        self.mapper = self.create_subscription(Float64MultiArray,'/interp2', self.mapCallBack1, 10)
        self.pub_1 = self.create_publisher(Twist, '/cmd_vel/bot2', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)
        self.pwms=Twist()
        self.pwms.linear.x=90.0
        self.pwms.linear.y=90.0
        self.pwms.linear.z=90.0
        self.pwm_right=90.0
        self.pwm_rear=90.0
        self.pwm_left=90.0
        self.w1=0.0
        self.w2=0.0
        self.w3=0.0


        self.pwms.angular.z=90.0
        

        
        self.rate = self.create_rate(100)
    
    def mapCallBack1(self, msg1):
        global sorted_pwm_right,sorted_rpm_right,sorted_rpm_left,sorted_pwm_left,sorted_rpm_rear,sorted_pwm_rear
        self.w1=msg1.data[0]
        self.w2=msg1.data[1]
        self.w3=msg1.data[2]

        self.pwm_right=np.interp(self.w1, sorted_rpm_right, sorted_pwm_right)
        self.pwm_left=np.interp(self.w2, sorted_rpm_left, sorted_pwm_left)
        self.pwm_rear=np.interp(self.w3, sorted_rpm_rear, sorted_pwm_rear)


    def timer_callback(self):
        self.pwms.linear.x=self.pwm_right
        self.pwms.linear.y=self.pwm_left
        self.pwms.linear.z=self.pwm_rear
        self.get_logger().info(f'right_rpm={self.w1} left_rpm={self.w2} rear_rpm={self.w3}')
        self.get_logger().info(f'right_pwm={self.pwms.linear.x} left_pwm={self.pwms.linear.y} rear_pwm={self.pwms.linear.z}')
        
        self.pub_1.publish(self.pwms)



    
    


def main(args=None):

    rclpy.init(args=args)
    
    # Create an instance of the HBController class
    hb_controller = interp()

    # Main loop
    while rclpy.ok():
        # Check if the service call is done
        
                ####################################################
        # hb_controller.get_logger().info("GOAL: no ")
        # Spin once to process callbacks
        rclpy.spin_once(hb_controller)
    
    # Destroy the node and shut down ROS
    hb_controller.destroy_node()
    rclpy.shutdown()






if __name__ == '__main__':
    main()    
