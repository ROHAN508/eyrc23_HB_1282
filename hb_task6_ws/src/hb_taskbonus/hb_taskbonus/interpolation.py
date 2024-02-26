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

rpmValues_right = [-42.55, -40.26, -35.714, -30.76, -21.66, -13.53, -10.60, -9.81, 0, 0, 0, 10.638, 13.495, 16.80, 25, 34.09, 42.55, 45.24, 46.9]
pwmValues_right = [180, 165, 150, 135, 120, 105, 100, 97, 96, 90, 88, 87, 80, 75, 60, 45, 30, 15, 0]

rpmValues_left= [-41.66, -39,76, -35.3, -30.30, -26.55, -20.54, -18.75, -13.63, -9.38,0.0, 0.0,0.0, 10.20, 13.27, 19.60, 24.9, 30.15, 33.33, 36.36, 40.7, 42.55, 43.17]
pwmValues_left= [180, 165, 155, 145, 135, 125, 115, 105, 97,96, 90,88, 87, 80, 70, 60, 50, 40, 30, 20, 10, 0]

rpmValues_rear= [-46.73, -44.77, -40.38, -35.30, -29.88, -24.3, -18.66, -13.5, -9.67,0.0,0.0,0.0, 10.31, 13.7, 19.67, 25.21, 30.93, 36.59, 41.66, 48, 49.2, 49.42]
pwmValues_rear= [180, 165, 155, 145, 135, 125, 115, 105, 97,96, 90, 88,87, 80, 70, 60, 50, 40, 30, 20, 10, 0]

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
        super().__init__('interpolator1')
        self.buffer=10
        self.mapper = self.create_subscription(Float64MultiArray,'/interp', self.mapCallBack1, self.buffer)
        self.pub_1 = self.create_publisher(Twist, '/cmd_vel/bot1', self.buffer)
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
        # self.get_logger().info(f'right_rpm={self.w1} left_rpm={self.w2} rear_rpm={self.w3}')
        # self.get_logger().info(f'right_pwm={self.pwms.linear.x} left_pwm={self.pwms.linear.y} rear_pwm={self.pwms.linear.z}')
        
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
