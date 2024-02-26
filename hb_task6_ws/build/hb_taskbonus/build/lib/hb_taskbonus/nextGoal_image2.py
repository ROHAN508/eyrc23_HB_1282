
import numpy as np
import matplotlib.pyplot as plt
from my_robot_interfaces.srv import NextGoal             
import rclpy
from rclpy.node import Node  
import random
import time
from my_robot_interfaces.msg import Goal           
from my_robot_interfaces.msg import Shape           
import math
from std_msgs.msg import Bool
from .image_utlis import *

spacing=5.0

msg_bot_2 =Goal()
fullimage2=[returncontour(24),returncontour(15),returncontour(16),returncontour(3),returncontour(1),returncontour(2),returncontour(4)]

pen_status_2=Bool()
pen_status_2.data=False
list_update_2=False

class ServiceNode(Node):

    def __init__(self):
        super().__init__('GOAL_node_img2')

        self.publish_goal_2 = self.create_publisher(Goal, 'hb_bot_2/goal_img', 10)

        self.run_complete2 = self.create_publisher(Bool, '/pen2_complete', 10)

        self.bot2_complete=Bool()
        self.bot2_complete.data=False

        self.pen_2_status = self.create_subscription(Bool, "/pen2_down", self.checkPenStatus_2, 10)
        

        self.resolution1=1
        self.resolution2=1
        self.resolution3=1
        self.scale=1
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        # self.get_logger().info(f'goal published')
        self.publish_goal_2.publish(msg_bot_2)
    
    def checkPenStatus_2(self,msg):
        global pen_status_2
        pen_status_2.data=msg.data


def main(args=None):
    rclpy.init(args=args)
    service_node = ServiceNode()
    
    global  msg_bot_2 
    

    image_idx=0

    while rclpy.ok():
        # service_node.get_logger().info(f'countour number bot2 :{image_idx}')
        if image_idx!=len(fullimage2):
            global list_update_2,pen_status_2
            if pen_status_2.data==False and list_update_2==False:
                msg_bot_2.bot_id = 2
                msg_bot_2.x = []
                msg_bot_2.y = []
                contour=fullimage2[image_idx]
                
                for coordinate in contour:
                    
                    msg_bot_2.x.append(coordinate[0])
                    msg_bot_2.y.append(coordinate[1]) 

                            
                msg_bot_2.theta = 0.0
                list_update_2=True
                image_idx+=1  
                service_node.get_logger().info(f'goal created')
                service_node.publish_goal_2.publish(msg_bot_2)
            # service_node.get_logger().info(msg_bot_2)

            if pen_status_2.data==True and list_update_2==True:
                list_update_2=False
        if image_idx==len(fullimage2):
            service_node.bot2_complete.data=True
            service_node.run_complete2.publish(service_node.bot2_complete) 
            service_node.get_logger().info(f'stup {service_node.bot2_complete}')       
        
            




            
        service_node.publish_goal_2.publish(msg_bot_2)    
            

        
        # time.sleep(1)
        rclpy.spin_once(service_node)
    rclpy.shutdown()
        
if __name__ == '__main__':
    main()

#######################################     DO NOT MODIFY THIS  FILE     ##########################################