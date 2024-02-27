
# ```
# * Team Id : HB#1282
# * Author List : AKSHAR DASH, ROHAN MOHAPATRA
# * Filename: nextGoal_function
# * Theme: HologlyphBots
# * Functions: generate_points
###########################



##import necessary modules
import numpy as np
import matplotlib.pyplot as plt
from my_robot_interfaces.srv import NextGoal             
import rclpy
from rclpy.node import Node  
import time
from my_robot_interfaces.msg import Goal           
from my_robot_interfaces.msg import Shape           
import math


class ServiceNode(Node):

    def __init__(self):

        ##create publisher for giving goals to bots
        super().__init__('GOAL_node')
        self.buffer=10
        self.publish_goal_1 = self.create_publisher(Goal, 'hb_bot_1/goal', self.buffer)
        self.publish_goal_2 = self.create_publisher(Goal, 'hb_bot_2/goal', self.buffer)
        self.publish_goal_3 = self.create_publisher(Goal, 'hb_bot_3/goal', self.buffer)

        ##define resolutionof the points
        self.resolution1=1
        self.resolution2=1
        self.resolution3=1
        ##define scale of the image
        self.scale=1


# ``
# * Function Name: generate_points
# * Output: lists of coordinates for goals of bot1,2 and 3
# * Logic: it iterates through all the theta and appends the coordinates to the respective lists

# * Example Call: ServiceNode.generate_points() 
        
    def generate_points(self):
        ##initialisation of goal coordinates
        coordinates_list1x = []
        coordinates_list1y = []
        coordinates_list2x = []
        coordinates_list2y = []
        coordinates_list3x = []
        coordinates_list3y = []
        ##loop to iterate through the angles
        for angle in range(0, 121, self.resolution1):
            t_rad = math.radians(angle)
            
            x1 = ((220 * math.cos(4*t_rad)*math.cos(t_rad)) / self.scale)+250
            y1 = ((220 * math.cos(4 * t_rad)*math.sin(t_rad)) / self.scale)+250
            coordinates_list1x.append(x1)
            coordinates_list1y.append(y1)

        for angle in range(120, 241, self.resolution2):
            t_rad = math.radians(angle)
        
            x2 = ((220 * math.cos(4*t_rad)*math.cos(t_rad)) / self.scale)+250
            y2 = ((220 * math.cos(4 * t_rad)*math.sin(t_rad)) / self.scale)+250
           
            coordinates_list2x.append(x2)
            coordinates_list2y.append(y2)

        for angle in range(240, 361, self.resolution3):
            t_rad = math.radians(angle)
        
            x3 = ((220 * math.cos(4*t_rad)*math.cos(t_rad)) / self.scale)+250
            y3 = ((220 * math.cos(4 * t_rad)*math.sin(t_rad)) / self.scale)+250
            coordinates_list3x.append(x3)
            coordinates_list3y.append(y3)



        return coordinates_list1x,coordinates_list1y,coordinates_list2x,coordinates_list2y,coordinates_list3x,coordinates_list3y      
    

def main(args=None):
    rclpy.init(args=args)
    service_node = ServiceNode()
    
    msg_bot_1 = Goal()
    msg_bot_2 = Goal()
    msg_bot_3 = Goal()
    


    ##for function mode
    msg_bot_1.x,msg_bot_1.y,msg_bot_2.x,msg_bot_2.y,msg_bot_3.x,msg_bot_3.y=service_node.generate_points()
    msg_bot_1.theta = 0.0
    msg_bot_2.theta = 0.0
    msg_bot_3.theta = 0.0
    msg_bot_1.bot_id = 1
    msg_bot_2.bot_id = 2
    msg_bot_3.bot_id = 3

    

    while rclpy.ok():
        ##publish the goals
        service_node.publish_goal_1.publish(msg_bot_1)    
        service_node.publish_goal_2.publish(msg_bot_2)    
        service_node.publish_goal_3.publish(msg_bot_3)    

        
        time.sleep(1)

    rclpy.shutdown()
        
if __name__ == '__main__':
    main()
