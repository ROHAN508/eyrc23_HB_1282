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

# max_rpm=35
max_rpm=37


class mapper(Node):
    def __init__(self):
        super().__init__('mapper2')
        self.buffer=10
        self.mapper = self.create_subscription(Float64MultiArray,'/map2', self.mapCallBack1, self.buffer)
        self.interp=self.create_publisher(Float64MultiArray,'/interp2',self.buffer)
        self.interpMsg=Float64MultiArray
        # self.w_max=0.0
        

        self.rate = self.create_rate(100)
    
    def mapCallBack1(self, msg1):
        global max_rpm
        self.w1=msg1.data[0]
        self.w2=msg1.data[1]
        self.w3=msg1.data[2]

        self.w_max=max(self.w1,self.w2,self.w3)
        if self.w1==0.0 and self.w2==0.0 and self.w3==0.0:

            self.interpMsg = Float64MultiArray()
            self.interpMsg.data = [self.w1, self.w2, self.w3]
            self.interp.publish(self.interpMsg)
        
        else:
            self.r1=self.w1/self.w_max
            self.r2=self.w2/self.w_max
            self.r3=self.w3/self.w_max

            self.w1=max_rpm*self.r1
            self.w2=max_rpm*self.r2
            self.w3=max_rpm*self.r3

            self.interpMsg = Float64MultiArray()
            self.interpMsg.data = [self.w1, self.w2, self.w3]
            self.interp.publish(self.interpMsg)



    
    


def main(args=None):

    rclpy.init(args=args)
    
    # Create an instance of the HBController class
    hb_controller = mapper()

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
