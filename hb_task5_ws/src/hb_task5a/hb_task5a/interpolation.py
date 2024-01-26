import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Wrench
from nav_msgs.msg import Odometry
import time
import math
import numpy as np
from std_msgs.msg import Bool
from tf_transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from my_robot_interfaces.msg import Goal             
from std_msgs.msg import Float64MultiArray
import numpy as np
import matplotlib.pyplot as plt

rpmValues_right = [-42.55, -40.26, -35.714, -30.76, -21.66, -13.53, -10.60, -9.81, 0, 0, 0, 10.638, 13.495, 16.80, 25, 34.09, 42.55, 45.24, 46.9]
pwmValues_right = [180, 165, 150, 135, 120, 105, 100, 97, 96, 90, 88, 87, 80, 75, 60, 45, 30, 15, 0]

rpmValues_left= [-41.66, -39,76, -35.3, -30.30, -26.55, -20.54, -18.75, -13.63, -9.38, 0, 10.20, 13.27, 19.60, 24.9, 30.15, 33.33, 36.36, 40.7, 42.55, 43.17]
pwmValues_left= [180, 165, 155, 145, 135, 125, 115, 105, 97, 90, 87, 80, 70, 60, 50, 40, 30, 20, 10, 0]

rpmValues_rear= [-46.73, -44.77, -40.38, -35.30, -29.88, -24.3, -18.66, -13.5, -9.67, 0, 10.31, 13.7, 19.67, 25.21, 30.93, 36.59, 41.66, 48, 49.2, 49.42]
pwmValues_rear= [180, 165, 155, 145, 135, 125, 115, 105, 97, 90, 87, 80, 70, 60, 50, 40, 30, 20, 10, 0]

# Remove duplicate RPM values
unique_indices = np.unique(rpmValues_right, return_index=True)[1]
unique_rpm = np.array(rpmValues_right)[unique_indices]
unique_pwm = np.array(pwmValues_right)[unique_indices]

# Sort the data
sorted_indices = np.argsort(unique_rpm)
sorted_rpm_right = unique_rpm[sorted_indices]
sorted_pwm_right = unique_pwm[sorted_indices]




class interp(Node):
    def __init__(self):
        super().__init__('interpolator1')
        
        self.mapper = self.create_subscription(Float64MultiArray,'/map', self.mapCallBack1, 10)
        # self.w_max=0.0
        self.rate = self.create_rate(100)
    
    def mapCallBack1(self, msg1):
        global sorted_pwm_right,sorted_rpm_right
        self.w1=msg1.data[0]
        self.w2=msg1.data[1]
        self.w3=msg1.data[2]

        self.pwm_right=np.interp(self.w1, sorted_rpm_right, sorted_pwm_right)


        



    
    


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
