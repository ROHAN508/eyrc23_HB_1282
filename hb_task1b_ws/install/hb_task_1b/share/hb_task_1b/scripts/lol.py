#!/usr/bin/env python3
import rclpy                                        # ROS 2 Python library for creating ROS 2 nodes
from rclpy.node import Node                         # Node class for creating ROS 2 nodes
from geometry_msgs.msg import Twist                   # Publishing to /cmd_vel with msg type: Twist
from nav_msgs.msg import Odometry                   # Subscribing to /odom with msg type: Odometry
import time                                          # Python time module for time-related functions
import math                                          # Python math module for mathematical functions
from tf_transformations import euler_from_quaternion # Odometry is given as a quaternion, but for the controller we'll need to find the orientaion theta by converting to euler angle
from my_robot_interfaces.srv import NextGoal          # Service

threshold=0.075

class HBTask1BController(Node):

    def __init__(self):
        super().__init__('hb_task1b_controller')
         
        # Initialze Publisher and Subscriber
        # We'll leave this for you to figure out the syntax for
        # initialising publisher and subscriber of cmd_vel and odom respectively
        self.pub= self.create_publisher(Twist, "/cmd_vel", 10)
        self.sub= self.create_subscription(Odometry, "/odom", self.odometryCb, 10)

        # Declare a Twist message
        self.vel = Twist()
        # Initialise the required variables to 0
        self.hb_x = 0.0
        self.hb_y = 0.0
        self.hb_theta = 0.0

        # For maintaining control loop rate.
        self.rate = self.create_rate(100)
        # Initialise variables that may be needed for the control loop
        # For ex: x_d, y_d, theta_d (in **meters** and **radians**) for defining desired goal-pose.
        # and also Kp values for the P Controller
        self.p=1
        self.t=5



        # client for the "next_goal" service
        self.cli = self.create_client(NextGoal, 'next_goal')      
        self.req = NextGoal.Request() 
        self.index = 0
        
    def odometryCb(self, msg):
        current_pos= msg.pose.pose.position
        self.hb_x = current_pos.x
        self.hb_y = current_pos.y
        rot_q = msg.pose.pose.orientation
        (_, _, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
        self.hb_theta = theta
        self.get_logger().info(f'{self.hb_x} {self.hb_y} theta={self.hb_theta}')

    # Write your code to take the msg and update the three variables

    def send_request(self, index):
        self.req.request_goal=index
        self.future = self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)
    
    # Create an instance of the EbotController class
    ebot_controller = HBTask1BController()
   
    # Send an initial request with the index from ebot_controller.index
    ebot_controller.send_request(ebot_controller.index)
    
    # Main loop
    while rclpy.ok():

        # Check if the service call is done
        if ebot_controller.future.done():
            try:
                # response from the service call
                response = ebot_controller.future.result()
            except Exception as e:
                ebot_controller.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                #########           GOAL POSE             #########
                x_goal      = response.x_goal
                y_goal      = response.y_goal
                theta_goal  = response.theta_goal
                ebot_controller.flag = response.end_of_list
                ebot_controller.get_logger().info(f"GOAL: {x_goal} {y_goal} {theta_goal}")
                ####################################################
                # Find error (in x, y and theta) in global frame
                # the /odom topic is giving pose of the robot in global frame
                # the desired pose is declared above and defined by you in global frame
                # therefore calculate error in global frame
                
                h=ebot_controller.hb_x
                k=ebot_controller.hb_y
                q=ebot_controller.hb_theta

                x_b= (x_goal-h)*(math.cos(q))+(y_goal-k)*(math.sin(q))
                y_b= (h-x_goal)*(math.sin(q))-(math.cos(q))*(k-y_goal)

                ebot_controller.vel.linear.x = ebot_controller.p*x_b
                ebot_controller.vel.linear.y = ebot_controller.p*y_b 
                distance= (x_b)**2 + (y_b)**2

                # (Calculate error in body frame)
                # But for Controller outputs robot velocity in robot_body frame, 
                # i.e. velocity are define is in x, y of the robot frame, 
                # Notice: the direction of z axis says the same in global and body frame
                # therefore the errors will have have to be calculated in body frame.
                # 
                # This is probably the crux of Task 1, figure this out and rest should be fine.

                # Finally implement a P controller 
                # to react to the error with velocities in x, y and theta.

                # Safety Check
                # make sure the velocities are within a range.
                # for now since we are in a simulator and we are not dealing with actual physical limits on the system 
                # we may get away with skipping this step. But it will be very necessary in the long run.


                #If Condition is up to you
            if distance < 0.01:    
                ############     DO NOT MODIFY THIS       #########
                ebot_controller.index += 1
                if ebot_controller.flag == 1 :
                    ebot_controller.index = 0
                ebot_controller.send_request(ebot_controller.index)
                time.sleep(1)
                ####################################################

        # Spin once to process callbacks
        rclpy.spin_once(ebot_controller)
    
    # Destroy the node and shut down ROS
    ebot_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
