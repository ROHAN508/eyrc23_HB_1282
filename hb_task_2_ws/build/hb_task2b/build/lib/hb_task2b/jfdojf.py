#! /usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		Hologlyph Bots (HB) Theme (eYRC 2023-24)
*        		===============================================
*
*  This script is to implement Task 2B of Hologlyph Bots (HB) Theme (eYRC 2023-24).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''


# Team ID:		[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:		feedback.py
# Functions:
#			[ Comma separated list of functions in this file ]
# Nodes:		Add your publishing and subscribing node


################### IMPORT MODULES #######################

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Wrench
import time
import math
import numpy as np
from tf_transformations import euler_from_quaternion
from my_robot_interfaces.msg import Goal             

p=15
d=15
distance_threshold= 1.0
theta_threshold=0.05
i=0


class HBController(Node):
    def __init__(self):
        super().__init__('hb_controller3')
        

        # Initialise the required variables
        self.bot_1_x_goal = []
        self.bot_1_y_goal = []
        self.bot_1_theta_goal = 0.0

        self.bot_1_x = 0.0
        self.bot_1_y = 0.0
        self.bot_1_theta = 0.0

        # Initialze Publisher and Subscriber
        # NOTE: You are strictly NOT-ALLOWED to use "cmd_vel" or "odom" topics in this task
	    #	Use the below given topics to generate motion for the robot.
	    #   /hb_bot_1/left_wheel_force,
	    #   /hb_bot_1/right_wheel_force,
	    #   /hb_bot_1/left_wheel_force

        self.subscription_bot1 = self.create_subscription(Goal,'hb_bot_3/goal', self.goalCallBack1, 10) 
        

        self.sub_bot_1 = self.create_subscription(Pose2D, '/detected_aruco_3', self.Callback1, 10)
        self.pub_bot1_1 = self.create_publisher(Wrench, '/hb_bot_3/right_wheel_force', 10)
        self.pub_bot1_2 = self.create_publisher(Wrench, '/hb_bot_3/left_wheel_force', 10)
        self.pub_bot1_3 = self.create_publisher(Wrench, '/hb_bot_3/rear_wheel_force', 10)

        

        # Similar to this you can create subscribers for hb_bot_2 and hb_bot_3
        

        # self.subscription  # Prevent unused variable warning

        # For maintaining control loop rate.
        self.rate = self.create_rate(100)

    def inverse_kinematics(self,xvel, yvel, ang_vel):
        ############ ADD YOUR CODE HERE ############

        # INSTRUCTIONS & HELP : 
        #	-> Use the target velocity you calculated for the robot in previous task, and
        #	Process it further to find what proportions of that effort should be given to 3 individuals wheels !!
        #	Publish the calculated efforts to actuate robot by applying force vectors on provided topics
        ############################################
        wheel_vel_1= (-0.33*xvel)+(0.58*yvel)+(0.33*ang_vel)
        wheel_vel_2= (-0.33*xvel)+(-0.58*yvel)+(0.33*ang_vel)
        wheel_vel_3= (0.66666*xvel)+(0.33333*ang_vel)
        return [wheel_vel_1, wheel_vel_2, wheel_vel_3]

    def goalCallBack1(self, msg1):
        self.bot_1_x_goal = msg1.x
        self.bot_1_y_goal = msg1.y
        self.bot_1_theta_goal = msg1.theta

    

    def Callback1(self, msg):
        self.bot_1_x = msg.x
        self.bot_1_y = msg.y
        self.bot_1_theta = msg.theta

   
def main(args=None):
    rclpy.init(args=args)
    
    hb_controller = HBController()
    global i
       
    # Main loop
    while rclpy.ok():

        # try:
        if hb_controller.bot_1_x_goal == []  and hb_controller.bot_1_x_goal == []:
            pass
        else:
            hb_controller.get_logger().info(f' X GOAL{hb_controller.bot_1_x_goal[i]}')
            hb_controller.get_logger().info(f'Y GOAL {hb_controller.bot_1_y_goal[i]}')
            # hb_controller.get_logger().info(f'CURRENT X{hb_controller.bot_1_x}')
            # hb_controller.get_logger().info(f'CURRENT Y{hb_controller.bot_1_y}')
        # hb_controller.get_logger().info(f'{hb_controller.bot_1_y_goal[i]}')
        
            x_goal= hb_controller.bot_1_x_goal[i]
            y_goal= hb_controller.bot_1_y_goal[i]
            theta_goal= hb_controller.bot_1_theta_goal


            h=hb_controller.bot_1_x
            k=hb_controller.bot_1_y
            q=hb_controller.bot_1_theta

            x_b= (x_goal-h)*(math.cos(q))+(y_goal-k)*(math.sin(q))
            y_b= (h-x_goal)*(math.sin(q))-(math.cos(q))*(k-y_goal)
            q_b= (q-theta_goal)*(-1)

            ang_vel_z = p*q_b+(d*np.sin(q_b))
            vel_x= p*x_b+(d*np.sign(x_b))
            vel_y= p*y_b +(d*np.sign(y_b))
            distance= ((x_b)**2 + (y_b)**2)**(0.5)

            req_forces = hb_controller.inverse_kinematics(vel_x, vel_y, ang_vel_z)

            msg_1 = Wrench()
            msg_1.force.x = 0.0
            msg_1.force.z = 0.0
            msg_1.force.y= req_forces[0]
            hb_controller.pub_bot1_1.publish(msg_1)

            msg_2 = Wrench()
            msg_2.force.x = 0.0
            msg_2.force.z = 0.0
            msg_2.force.y = req_forces[1]
            hb_controller.pub_bot1_2.publish(msg_2)

            msg_3 = Wrench()
            msg_3.force.x = 0.0
            msg_3.force.z = 0.0
            msg_3.force.y = req_forces[2]
            hb_controller.pub_bot1_3.publish(msg_3)

            hb_controller.get_logger().info(f'{distance}')
            
            if distance < distance_threshold:
                i = i+1
            if i==len(hb_controller.bot_1_x_goal):
                msg_1.force.y= 0.0
                hb_controller.pub_bot1_1.publish(msg_1)
                msg_2.force.y = 0.0
                hb_controller.pub_bot1_2.publish(msg_2)
                msg_3.force.y = 0.0
                hb_controller.pub_bot1_3.publish(msg_3)
                break     
     

        rclpy.spin_once(hb_controller)
    
    # Destroy the node and shut down ROS
    hb_controller.destroy_node()
    rclpy.shutdown()

# Entry point of the script
if __name__ == '__main__':
    main()
