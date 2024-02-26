
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



class ServiceNode(Node):

    def __init__(self):
        super().__init__('GOAL_node')
        self.buffer=10
        self.publish_goal_1 = self.create_publisher(Goal, 'hb_bot_1/goal', self.buffer)
        self.publish_goal_2 = self.create_publisher(Goal, 'hb_bot_2/goal', self.buffer)
        self.publish_goal_3 = self.create_publisher(Goal, 'hb_bot_3/goal', self.buffer)
        
        # self.publish_shape_1  = self.create_publisher(Shape, 'shape_1', 10)
        # self.publish_shape_2  = self.create_publisher(Shape, 'shape_2', 10)
        # self.publish_shape_3  = self.create_publisher(Shape, 'shape_3', 10)
        self.resolution1=1
        self.resolution2=1
        self.resolution3=1
        self.scale=1


    def generate_points(self):
        coordinates_list1x = []
        coordinates_list1y = []
        coordinates_list2x = []
        coordinates_list2y = []
        coordinates_list3x = []
        coordinates_list3y = []

        for angle in range(0, 121, self.resolution1):
            t_rad = math.radians(angle)
            # x1 = (200 * math.cos(t_rad)) / self.scale
            # y1 = (150 * math.sin(4 * t_rad)) / self.scale
            x1 = ((220 * math.cos(4*t_rad)*math.cos(t_rad)) / self.scale)+250
            y1 = ((220 * math.cos(4 * t_rad)*math.sin(t_rad)) / self.scale)+250
            coordinates_list1x.append(x1)
            coordinates_list1y.append(y1)

        for angle in range(120, 241, self.resolution2):
            t_rad = math.radians(angle)
            # x2 = (200 * math.cos(t_rad)) / self.scale
            # y2 = (150 * math.sin(4 * t_rad)) / self.scale
            x2 = ((220 * math.cos(4*t_rad)*math.cos(t_rad)) / self.scale)+250
            y2 = ((220 * math.cos(4 * t_rad)*math.sin(t_rad)) / self.scale)+250
           
            coordinates_list2x.append(x2)
            coordinates_list2y.append(y2)

        for angle in range(240, 361, self.resolution3):
            t_rad = math.radians(angle)
            # x3 = (200 * math.cos(t_rad)) / self.scale
            # y3 = (150 * math.sin(4 * t_rad)) / self.scale
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

    # msg_shape = Shape()
    # msg_shape_2 = Shape()
    # msg_shape_3 = Shape()

    
    # #5a
    # msg_bot_1.bot_id = 1
    # msg_bot_1.x = []
    # msg_bot_1.y = []
    # for coordinate in hexagon_points:
    #    msg_bot_1.x.append(coordinate[0])
    #    msg_bot_1.y.append(coordinate[1]) 
    
    # msg_bot_1.theta = 0.0

    # msg_bot_2.bot_id = 2
    # msg_bot_2.x = []
    # msg_bot_2.y = []

    # for coordinate in rectangle_points:
    #    msg_bot_2.x.append(coordinate[0])
    #    msg_bot_2.y.append(coordinate[1]) 
    
    # msg_bot_2.theta = 0.0

    # msg_bot_3.bot_id = 3
    # msg_bot_3.x = []
    # msg_bot_3.y = []

    # for coordinate in triangle_points:
    #    msg_bot_3.x.append(coordinate[0])
    #    msg_bot_3.y.append(coordinate[1]) 

    # msg_bot_3.theta = 0.0


    ##5b
    msg_bot_1.x,msg_bot_1.y,msg_bot_2.x,msg_bot_2.y,msg_bot_3.x,msg_bot_3.y=service_node.generate_points()
    msg_bot_1.theta = 0.0
    msg_bot_2.theta = 0.0
    msg_bot_3.theta = 0.0
    msg_bot_1.bot_id = 1
    msg_bot_2.bot_id = 2
    msg_bot_3.bot_id = 3

    

    while rclpy.ok():

        service_node.publish_goal_1.publish(msg_bot_1)    
        service_node.publish_goal_2.publish(msg_bot_2)    
        service_node.publish_goal_3.publish(msg_bot_3)    

        
        time.sleep(1)

    rclpy.shutdown()
        
if __name__ == '__main__':
    main()
