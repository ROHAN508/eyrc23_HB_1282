#######################################     DO NOT MODIFY THIS  FILE     ##########################################
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

hexagon_points=[[200, 150], [175, 200], [125, 200], [100, 150], [125, 100], [175, 100],[200, 150]]

triangle_points=[[300, 100], [400, 100],[300, 200], [300, 100]]


# rectangle_points= [[200, 300],[250,300],[300,300] ,[350,300],[400, 300],[400,350], [400, 400],[375,400],[350,400],[325,400],[300,400],[275,400],[250,400],[225,400], [200, 400],[200,350], [200, 300]]
rectangle_points= [[200, 300],[250,300],[300,300] ,[350,300],[400, 300],[400,350], [400, 400],[300,400], [200, 400],[200,350], [200, 300]]


class ServiceNode(Node):

    def __init__(self):
        super().__init__('GOAL_node')

        self.publish_goal_1 = self.create_publisher(Goal, 'hb_bot_1/goal', 10)
        self.publish_goal_2 = self.create_publisher(Goal, 'hb_bot_2/goal', 10)
        self.publish_goal_3 = self.create_publisher(Goal, 'hb_bot_3/goal', 10)
        
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
    





def generate_decagon(side_length, x_center, y_center, theta, num_points):
    angles = np.linspace(0, 2 * np.pi, 10, endpoint=False) + theta
    x_vertices = x_center + side_length * np.cos(angles)
    y_vertices = y_center + side_length * np.sin(angles)
    
    x_points = np.linspace(x_vertices[-1], x_vertices[0], num_points)
    y_points = np.linspace(y_vertices[-1], y_vertices[0], num_points)
    
    x_interp = np.interp(np.linspace(0, 1, num_points), np.linspace(0, 1, 10), x_vertices)
    y_interp = np.interp(np.linspace(0, 1, num_points), np.linspace(0, 1, 10), y_vertices)
    
    return x_interp.tolist(), y_interp.tolist(), theta

def generate_triangle(side_length, x_center, y_center, theta, num_points):

    height = (np.sqrt(3) / 2) * side_length
    
    x_vertices = np.array([0, side_length / 2, -side_length / 2, 0])
    y_vertices = np.array([height / 2, -height / 2, -height / 2, height / 2])
    
    x_rot = x_vertices * np.cos(theta) - y_vertices * np.sin(theta)
    y_rot = x_vertices * np.sin(theta) + y_vertices * np.cos(theta)
    
    x = x_center + x_rot
    y = y_center + y_rot
    
    x_left = np.linspace(x[2], x[0], num_points // 3)
    y_left = np.linspace(y[2], y[0], num_points // 3)
    x_right = np.linspace(x[0], x[1], num_points // 3)
    y_right = np.linspace(y[0], y[1], num_points // 3)
    x_bottom = np.linspace(x[1], x[2], num_points // 3)
    y_bottom = np.linspace(y[1], y[2], num_points // 3)
    
    x = np.concatenate((x_left, x_right[1:], x_bottom[1:]))
    y = np.concatenate((y_left, y_right[1:], y_bottom[1:]))
    
    return x.tolist(), y.tolist(), theta

def generate_square(side_length, x_center, y_center, theta, num_points):
    half_length = side_length / 2
    
    x_vertices = np.array([-half_length, half_length, half_length, -half_length, -half_length])
    y_vertices = np.array([-half_length, -half_length, half_length, half_length, -half_length])
    
    x_rot = x_vertices * np.cos(theta) - y_vertices * np.sin(theta)
    y_rot = x_vertices * np.sin(theta) + y_vertices * np.cos(theta)
    
    x = x_center + x_rot
    y = y_center + y_rot
    
    x_left = np.linspace(x[3], x[0], num_points // 4)
    y_left = np.linspace(y[3], y[0], num_points // 4)
    x_top = np.linspace(x[0], x[1], num_points // 4)
    y_top = np.linspace(y[0], y[1], num_points // 4)
    x_right = np.linspace(x[1], x[2], num_points // 4)
    y_right = np.linspace(y[1], y[2], num_points // 4)
    x_bottom = np.linspace(x[2], x[3], num_points // 4)
    y_bottom = np.linspace(y[2], y[3], num_points // 4)
    
    x = np.concatenate((x_left, x_top[1:], x_right[1:], x_bottom[1:]))
    y = np.concatenate((y_left, y_top[1:], y_right[1:], y_bottom[1:]))
    
    return x.tolist(), y.tolist(), theta


def main(args=None):
    rclpy.init(args=args)
    service_node = ServiceNode()

    # tri_side_length = np.random.randint(50, 101)
    # sq_side_length  = np.random.randint(50, 101)
    # dec_side_length = np.random.randint(50, 101)

    # # Generate random rotation angles for the shapes between 0 and 2*pi
    # tri_theta = np.random.uniform(0, 2*np.pi)
    # sq_theta  = np.random.uniform(0, 2*np.pi)
    # dec_theta = np.random.uniform(0, 2*np.pi)

    # shape1_x,shape1_y,shape1_theta  = generate_triangle((tri_side_length), 350, 150, (tri_theta), 100)
    # shape2_x,shape2_y,shape2_theta  = generate_square(sq_side_length, 150, 250, sq_theta, 100)
    # shape3_x,shape3_y,shape3_theta  = generate_decagon(dec_side_length, 400, 400, dec_theta, 100)
    
    msg_bot_1 = Goal()
    msg_bot_2 = Goal()
    msg_bot_3 = Goal()

    # msg_shape = Shape()
    # msg_shape_2 = Shape()
    # msg_shape_3 = Shape()

    
    # #5a
    msg_bot_1.bot_id = 1
    msg_bot_1.x = []
    msg_bot_1.y = []
    for coordinate in hexagon_points:
       msg_bot_1.x.append(coordinate[0])
       msg_bot_1.y.append(coordinate[1]) 
    
    msg_bot_1.theta = 0.0

    msg_bot_2.bot_id = 2
    msg_bot_2.x = []
    msg_bot_2.y = []

    for coordinate in rectangle_points:
       msg_bot_2.x.append(coordinate[0])
       msg_bot_2.y.append(coordinate[1]) 
    
    msg_bot_2.theta = 0.0

    msg_bot_3.bot_id = 3
    msg_bot_3.x = []
    msg_bot_3.y = []

    for coordinate in triangle_points:
       msg_bot_3.x.append(coordinate[0])
       msg_bot_3.y.append(coordinate[1]) 

    msg_bot_3.theta = 0.0


    ##5b
    # msg_bot_1.x,msg_bot_1.y,msg_bot_2.x,msg_bot_2.y,msg_bot_3.x,msg_bot_3.y=service_node.generate_points()
    # msg_bot_1.theta = 0.0
    # msg_bot_2.theta = 0.0
    # msg_bot_3.theta = 0.0
    # msg_bot_1.bot_id = 1
    # msg_bot_2.bot_id = 2
    # msg_bot_3.bot_id = 3

    

    while rclpy.ok():

        service_node.publish_goal_1.publish(msg_bot_1)    
        service_node.publish_goal_2.publish(msg_bot_2)    
        service_node.publish_goal_3.publish(msg_bot_3)    
    
        # service_node.publish_shape_1.publish(msg_shape_1)
        # service_node.publish_shape_2.publish(msg_shape_2)
        # service_node.publish_shape_3.publish(msg_shape_3)
        
        time.sleep(1)

    rclpy.shutdown()
        
if __name__ == '__main__':
    main()

#######################################     DO NOT MODIFY THIS  FILE     ##########################################