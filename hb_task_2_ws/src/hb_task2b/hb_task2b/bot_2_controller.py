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
# Nodes:		Publshing nodes:HBController2.pub_bot2_1
#                               HBController2.pub_bot2_2
#                               HBController2.pub_bot2_3
#              Subscribing nodes: HBController.sub_bot_2                       


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
from my_robot_interfaces.msg import Goal             

# You can add more if required
##############################################################


# Initialize Global variables
k_p=15 #proportional constant
d=15 #some force so that the bot does not completely stop
k_d=5 #derivative constant
theta_prev_er=0.0 #previous error in theta
theta_pres_er=0.0 #present error in theta
previous_error=0.0 #previous error in distance
present_error=0.0 # present error in distance
distance_threshold=1
theta_threshold=0.15
i=0 #index variable
max_speed=20
max_error=30
r=1.9
dc=7.0
################# ADD UTILITY FUNCTIONS HERE #################
#function to calculate forces of each wheel using p and d controller
def forces(x_b,y_b,q_b):
    force_z = k_p*q_b+(d*np.sign(q_b))+k_d*(theta_prev_er-theta_pres_er)*(-1)
    force_x= k_p*x_b+(d*np.sign(x_b))+k_d*(previous_error-present_error)*(-1)
    force_y= k_p*y_b +(d*np.sign(y_b))+k_d*(previous_error-present_error)*(-1)

    return [force_x,force_y,force_z]
def speed_cap(x_b,y_b):
    if (abs(x_b)>max_error):
        k= x_b/y_b
        x_b=max_speed*np.sign(x_b)
        y_b=x_b/k
    if abs(y_b)>max_error:
        k=x_b/y_b
        y_b=max_speed*np.sign(y_b)
        x_b=k*y_b    
    return [x_b,y_b]   
##############################################################

# Define the HBController class, which is a ROS node
class HBController2(Node):
    def __init__(self):
        super().__init__('hb_controller2')
        

        # Initialise the required variables
        self.bot_2_x_goal = []
        self.bot_2_y_goal = []
        self.bot_2_theta_goal = 0.0

        self.bot_2_x = 0.0
        self.bot_2_y = 0.0
        self.bot_2_theta = 0.0

        # Initialze Publisher and Subscriber
        # NOTE: You are strictly NOT-ALLOWED to use "cmd_vel" or "odom" topics in this task
	    #	Use the below given topics to generate motion for the robot.
	    #   /hb_bot_1/left_wheel_force,
	    #   /hb_bot_1/right_wheel_force,
	    #   /hb_bot_1/left_wheel_force

        self.subscription_bot2 = self.create_subscription(Goal,'hb_bot_2/goal', self.goalCallBack1, 10) 
        

        self.sub_bot_2 = self.create_subscription(Pose2D, '/detected_aruco_2', self.Callback1, 10)
        self.pub_bot2_1 = self.create_publisher(Wrench, '/hb_bot_2/right_wheel_force', 10)
        self.pub_bot2_2 = self.create_publisher(Wrench, '/hb_bot_2/left_wheel_force', 10)
        self.pub_bot2_3 = self.create_publisher(Wrench, '/hb_bot_2/rear_wheel_force', 10)

        

        # Similar to this you can create subscribers for hb_bot_2 and hb_bot_3
        

        # self.subscription  # Prevent unused variable warning

        # For maintaining control loop rate.
        self.rate = self.create_rate(100)
    
    # Method to create a request to the "next_goal" service
    
        

    def inverse_kinematics(self,xvel, yvel, ang_vel):
        ############ ADD YOUR CODE HERE ############

        # INSTRUCTIONS & HELP : 
        #	-> Use the target velocity you calculated for the robot in previous task, and
        #	Process it further to find what proportions of that effort should be given to 3 individuals wheels !!
        #	Publish the calculated efforts to actuate robot by applying force vectors on provided topics
        ############################################
        # wheel_vel_1= (-0.33*xvel)+(0.58*yvel)+(0.33*ang_vel)
        # wheel_vel_2= (-0.33*xvel)+(-0.58*yvel)+(0.33*ang_vel)
        # wheel_vel_3= (0.66666*xvel)+(0.33333*ang_vel)
        # w1_vel = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (0.866*yvel))
        # w2_vel = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (-0.866*yvel))
        # w3_vel = (1/r) * ((ang_vel*dc) + (1*xvel) + (0*yvel))
        wheel_vel_1= (1/r)*(-0.33*xvel)+(0.58*yvel)+(0.04762*ang_vel)
        wheel_vel_2= (1/r)*(-0.33*xvel)+(-0.58*yvel)+(0.04762*ang_vel)
        wheel_vel_3= (1/r)*(0.66666*xvel)+(0.04762*ang_vel)
        return [wheel_vel_1, wheel_vel_2, wheel_vel_3]

    def goalCallBack1(self, msg1):
        self.bot_2_x_goal = msg1.x
        self.bot_2_y_goal = msg1.y
        self.bot_2_theta_goal = msg1.theta

    

    def Callback1(self, msg):
        self.bot_2_x = msg.x
        self.bot_2_y = msg.y
        self.bot_2_theta = msg.theta

    def errors(self,x_goal,y_goal,theta_goal):
        h=self.bot_2_x
        k=self.bot_2_y
        q=self.bot_2_theta
        # transformations with respect to the bot frame.
        x_b= (x_goal-h)*(math.cos(q))+(y_goal-k)*(math.sin(q)) #error in x value
        y_b= (h-x_goal)*(math.sin(q))-(math.cos(q))*(k-y_goal) #error in y value
        q_b= (q-theta_goal)*(-1) #error in theta value
        distance= ((x_b)**2 + (y_b)**2)**(0.5) #distance of bot from goal pose
        return [x_b,y_b,q_b,distance]
        
def main(args=None):

    rclpy.init(args=args)
    
    # Create an instance of the HBController class
    hb_controller2 = HBController2()
   
    global i
    # Main loop
    while rclpy.ok():

        # Check if the service call is done
        if hb_controller2.bot_2_x_goal == []  and hb_controller2.bot_2_x_goal == []:
            pass
        else:
                #########           GOAL POSE             #########
                x_goal= hb_controller2.bot_2_x_goal[i]
                y_goal= hb_controller2.bot_2_y_goal[i]
                theta_goal= hb_controller2.bot_2_theta_goal
                ####################################################
                if theta_goal>math.pi:
                    theta_goal=theta_goal-(2*math.pi)
                # Calculate Error from feedback
                global present_error,previous_error,theta_prev_er,theta_pres_er
                #caculate the errors from goal pose and present pose
                x_b, y_b, q_b, distance= hb_controller2.errors(x_goal,y_goal,theta_goal)
                present_error= distance
                theta_pres_er=q_b
                x_b,y_b=speed_cap(x_b,y_b)
                #caculate force required in x,y and theta by using errors from goal.
                force_list=forces(x_b,y_b,q_b)
                previous_error=present_error
                theta_prev_er=theta_pres_er
                #caculate the forces required for each wheel by using inverse kinematics.
                req_forces = hb_controller2.inverse_kinematics(force_list[0],force_list[1],force_list[2])
                #publish the calculated forces.
                msg_1 = Wrench()
                msg_1.force.x = 0.0
                msg_1.force.z = 0.0
                msg_1.force.y= req_forces[0]
                hb_controller2.pub_bot2_1.publish(msg_1)

                msg_2 = Wrench()
                msg_2.force.x = 0.0
                msg_2.force.z = 0.0
                msg_2.force.y = req_forces[1]
                hb_controller2.pub_bot2_2.publish(msg_2)

                msg_3 = Wrench()
                msg_3.force.x = 0.0
                msg_3.force.z = 0.0
                msg_3.force.y = req_forces[2]
                hb_controller2.pub_bot2_3.publish(msg_3)
                # hb_controller2.get_logger().info(f'{theta_goal}')

                # Change the frame by using Rotation Matrix (If you find it required)

                # Calculate the required velocity of bot for the next iteration(s)
                
                # Find the required force vectors for individual wheels from it.(Inverse Kinematics)

                # Apply appropriate force vectors

                # Modify the condition to Switch to Next goal (given position in pixels instead of meters)
                if distance < distance_threshold and q_b < theta_threshold:
                    i = i+1
                if i==len(hb_controller2.bot_2_x_goal):
                    msg_1.force.y= 0.0
                    hb_controller2.pub_bot2_1.publish(msg_1)
                    msg_2.force.y = 0.0
                    hb_controller2.pub_bot2_2.publish(msg_2)
                    msg_3.force.y = 0.0
                    hb_controller2.pub_bot2_3.publish(msg_3)
                    break     
                    ####################################################
        # hb_controller.get_logger().info("GOAL: no ")
        # Spin once to process callbacks
        rclpy.spin_once(hb_controller2)
    
    # Destroy the node and shut down ROS
    hb_controller2.destroy_node()
    rclpy.shutdown() 

# Entry point of the script
if __name__ == '__main__':
    main()