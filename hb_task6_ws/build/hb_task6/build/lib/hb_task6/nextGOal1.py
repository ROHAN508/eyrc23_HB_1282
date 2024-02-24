import cv2
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
import ast

class ServiceNode(Node):

    def __init__(self):
        super().__init__('GOAL_node')

        self.publish_goal_1 = self.create_publisher(Goal, 'hb_bot_2/goal', 10)

        self.resolution1=1
        self.resolution2=1
        self.resolution3=1
        self.scale=1


    def read_contour_coordinates(self, file_path):
        contour_coordinates = []
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('Contour'):
                    contour_str = line.split(': ')[1].strip()
                    contour_coordinates.append(ast.literal_eval(contour_str))
        return contour_coordinates

    def publish_coordinates(self, msg_bot, coordinates):
        msg_bot.x = []
        msg_bot.y = []
        for coordinate in coordinates:
            msg_bot.x.append(coordinate[0])
            msg_bot.y.append(coordinate[1]) 

    def main(self):
        msg_bot_1 = Goal()

        contour_coordinates = self.read_contour_coordinates('contours_coordinates.txt')

        for coordinates in contour_coordinates:
            self.publish_coordinates(msg_bot_1, coordinates)

        while rclpy.ok():
            self.publish_goal_1.publish(msg_bot_1)
            time.sleep(1)

        rclpy.shutdown()


def main(args=None):
    rclpy.init()  # Initialize rclpy only once in the main function
    service_node = ServiceNode()
    service_node.main()

if __name__ == '__main__':
    main()
