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

rpmValues_right = [-47.32, -47.32, -42.55, -38.61, -31.75, -26.786, -22.156, -15.61, -9.19, 0.0, 0.0, 0.0, 0.0, 0.0, 9.85, 13.02, 19.74, 25.707, 30.4, 37.27, 42.135, 47.1, 49.59, 50]
pwmValues_right = [180, 170, 160, 150, 140, 130, 120, 110, 97, 96, 92, 90, 89, 88, 87, 80, 70, 60, 50, 40, 30, 20, 10, 0]

rpmValues_rear= [-38.96,-34.88,-31.5789,-24.49,-12.18,0.0,0.0,0.0,12.766,20.52,29.85,33.52,38.96]
pwmValues_rear=   [140,130, 120, 110, 99, 95, 90, 88, 87, 80, 70, 60, 50]

rpmValues_left= [-48, -46.875, -43.04, -37.83, -32.644, -26.55, -21.82, -15.53, -10.58, 0.0, 0.0, 0.0, 0.0, 10, 14.03, 20.72, 25.86, 30.61, 37.5, 41.78, 47.47, 48.39, 49.67]
pwmValues_left= [180, 170, 160, 150, 140, 130, 120, 110, 99, 96, 92, 90, 89, 88, 80, 70, 60, 50, 40, 30, 20, 10, 0]

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
        super().__init__('interpolator3')
        
        self.mapper = self.create_subscription(Float64MultiArray,'/interp3', self.mapCallBack1, 10)
        self.pub_1 = self.create_publisher(Twist, '/cmd_vel/bot3', 10)
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
