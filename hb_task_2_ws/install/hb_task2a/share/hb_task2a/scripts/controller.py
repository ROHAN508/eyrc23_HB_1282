#! /usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		Hologlyph Bots (HB) Theme (eYRC 2023-24)
*        		===============================================
*
*  This script is to implement Task 2A of Hologlyph Bots (HB) Theme (eYRC 2023-24).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''


# Team ID:		1282
# Author List:	Akshar Dash, Rohan Mohapatra
# Filename:		controller.py
# Functions:
#			[ forces,send_request,inverse_kinematics,callback,errors]
# Nodes:		Publshing nodes:HBController.pub_1
#                               HBController.pub_2
#                               HBController.pub_3
#              Subsribing nodes:HBController.sub                       


################### IMPORT MODULES #######################

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Wrench
from nav_msgs.msg import Odometry
import time
import math
import numpy as np
from tf_transformations import euler_from_quaternion
from my_robot_interfaces.srv import NextGoal             

# You can add more if required
##############################################################


# Initialize Global variables
k_p=15 #proportional constant
d=10 #some force so that the bot does not completely stop
k_d=15 #derivative constant
theta_prev_er=0 #previous error in theta
theta_pres_er=0 #present error in theta
previous_error=0.0 #previous error in distance
present_error=0.0 # present error in distance
distance_threshold=0.4
theta_threshold=0.05

################# ADD UTILITY FUNCTIONS HERE #################
#function to calculate forces of each wheel using p and d controller
def forces(x_b,y_b,q_b):
    force_z = k_p*q_b+(d*np.sign(q_b))+k_d*(theta_prev_er-theta_pres_er)*(-1)
    force_x= k_p*x_b+(d*np.sign(x_b))+k_d*(previous_error-present_error)*(-1)
    force_y= k_p*y_b +(d*np.sign(y_b))+k_d*(previous_error-present_error)*(-1)

    return [force_x,force_y,force_z]
##############################################################

# Define the HBController class, which is a ROS node
class HBController(Node):
    def __init__(self):
        super().__init__('hb_controller')
        
        # Initialze Publisher and Subscriber
        # NOTE: You are strictly NOT-ALLOWED to use "cmd_vel" or "odom" topics in this task
	    #	Use the below given topics to generate motion for the robot.
	    #   /hb_bot_1/left_wheel_force,
	    #   /hb_bot_1/right_wheel_force,
	    #   /hb_bot_1/left_wheel_force
        #subscribes to the detected_aruco topic.
        self.sub = self.create_subscription(Pose2D, '/detected_aruco', self.callback, 10)
        self.pub_1 = self.create_publisher(Wrench, '/hb_bot_1/right_wheel_force', 10)
        self.pub_2 = self.create_publisher(Wrench, '/hb_bot_1/left_wheel_force', 10)
        self.pub_3 = self.create_publisher(Wrench, '/hb_bot_1/rear_wheel_force', 10)


        # For maintaining control loop rate.
        self.rate = self.create_rate(100)
        #initialise attributes for bot localisation.
        self.bot_x = 0.0
        self.bot_y = 0.0
        self.bot_theta = 0.0

        # client for the "next_goal" service
        self.cli = self.create_client(NextGoal, 'next_goal')      
        self.req = NextGoal.Request() 
        self.index = 0

    
    # Method to create a request to the "next_goal" service
    def send_request(self, request_goal):
        self.req.request_goal = request_goal
        self.future = self.cli.call_async(self.req)
        

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

    def callback(self, msg):
        self.bot_x = msg.x
        self.bot_y = msg.y
        self.bot_theta = msg.theta
        self.get_logger().info(f'info : {self.bot_x},{self.bot_y},{self.bot_theta}')

    def errors(self,x_goal,y_goal,theta_goal):
        h=self.bot_x
        k=self.bot_y
        q=self.bot_theta
        # transformations with respect to the bot frame.
        x_b= (x_goal-h)*(math.cos(q))+(y_goal-k)*(math.sin(q)) #error in x value
        y_b= (h-x_goal)*(math.sin(q))-(math.cos(q))*(k-y_goal) #error in y value
        q_b= (q-theta_goal)*(-1) #error in theta value
        distance= ((x_b)**2 + (y_b)**2)**(0.5) #distance of bot from goal pose
        return [x_b,y_b,q_b,distance]
        
def main(args=None):

    rclpy.init(args=args)
    
    # Create an instance of the HBController class
    hb_controller = HBController()
   
    # Send an initial request with the index from ebot_controller.index
    hb_controller.send_request(hb_controller.index)
    
    # Main loop
    while rclpy.ok():

        # Check if the service call is done
        if hb_controller.future.done():
            try:
                # response from the service call
                response = hb_controller.future.result()
            except Exception as e:
                hb_controller.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                #########           GOAL POSE             #########
                x_goal      = response.x_goal + 250
                y_goal      = response.y_goal + 250
                theta_goal  = response.theta_goal
                hb_controller.flag = response.end_of_list
                hb_controller.get_logger().info(f"GOAL: {(x_goal)} {(y_goal)} {theta_goal}")
                ####################################################
                
                # Calculate Error from feedback
                global present_error,previous_error,theta_prev_er,theta_pres_er
                #caculate the errors from goal pose and present pose
                x_b, y_b, q_b, distance= hb_controller.errors(x_goal,y_goal,theta_goal)
                present_error= distance
                theta_pres_er=q_b
                #caculate force required in x,y and theta by using errors from goal.
                force_list=forces(x_b,y_b,q_b)
                previous_error=present_error
                theta_prev_er=theta_pres_er
                #caculate the forces required for each wheel by using inverse kinematics.
                req_forces = hb_controller.inverse_kinematics(force_list[0],force_list[1],force_list[2])
                #publish the calculated forces.
                msg_1 = Wrench()
                msg_1.force.x = 0.0
                msg_1.force.z = 0.0
                msg_1.force.y= req_forces[0]
                hb_controller.pub_1.publish(msg_1)

                msg_2 = Wrench()
                msg_2.force.x = 0.0
                msg_2.force.z = 0.0
                msg_2.force.y = req_forces[1]
                hb_controller.pub_2.publish(msg_2)

                msg_3 = Wrench()
                msg_3.force.x = 0.0
                msg_3.force.z = 0.0
                msg_3.force.y = req_forces[2]
                hb_controller.pub_3.publish(msg_3)

                # Change the frame by using Rotation Matrix (If you find it required)

                # Calculate the required velocity of bot for the next iteration(s)
                
                # Find the required force vectors for individual wheels from it.(Inverse Kinematics)

                # Apply appropriate force vectors

                # Modify the condition to Switch to Next goal (given position in pixels instead of meters)
                if distance < distance_threshold and q_b < theta_threshold:        
                    ############     DO NOT MODIFY THIS       #########
                    hb_controller.index += 1
                    if hb_controller.flag == 1 :
                        hb_controller.index = 0
                    hb_controller.send_request(hb_controller.index)
                    ####################################################
        # hb_controller.get_logger().info("GOAL: no ")
        # Spin once to process callbacks
        rclpy.spin_once(hb_controller)
    
    # Destroy the node and shut down ROS
    hb_controller.destroy_node()
    rclpy.shutdown() 

# Entry point of the script
if __name__ == '__main__':
    main()