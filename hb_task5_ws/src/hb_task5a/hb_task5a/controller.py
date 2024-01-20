import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Wrench
from nav_msgs.msg import Odometry
import time
import math
import numpy as np
from std_msgs.msg import Bool
from tf_transformations import euler_from_quaternion
from geometry_msgs.msg import Twist

pen_down=False
distance_threshold=1.5
forward_vel=[25.0,180.0,90.0]
clockwise=[0.0,0.0,0.0]
anticlockwise=[180.0,180.0,180.0]

class HBControl(Node):
    def __init__(self):
        super().__init__('hb_controller')
        

        # Initialise the required variables
        self.bot_x_goal = []
        self.bot_y_goal = []
        # self.bot_3_theta_goal = 0.0

        self.bot_x = 0.0
        self.bot_y = 0.0
        self.bot_theta = 0.0

        # self.subscription_bot3 = self.create_subscription(Goal,'hb_bot_3/goal', self.goalCallBack1, 10) 
        

        self.sub_bot_1 = self.create_subscription(Pose2D, "/pen1_pose", self.Callback1, 10)
        self.twist_1 =  Twist()
        self.pen1=Bool()
        self.pen1.data=False
        
        self.pub_1 = self.create_publisher(Twist, '/cmd_vel/bot1', 10)
        self.pen_pub1 = self.create_publisher(Bool, '/pen1_down', 10)

        self.rate = self.create_rate(100)
    
    def Callback1(self, msg):
        self.bot_x = msg.x
        self.bot_y = msg.y
        self.bot_theta = msg.theta

    def moveforward(self,flag):
        global forward_vel
        if flag==True:
            self.twist_1.linear.x=forward_vel[0]
            self.twist_1.linear.y=forward_vel[1]
            self.twist_1.linear.z=forward_vel[2] 
        if flag==False:
            self.twist_1.linear.x=90.0
            self.twist_1.linear.y=90.0
            self.twist_1.linear.z=90.0
    def rotate(self,num):
        global clockwise, anticlockwise
        if num==0:
            self.twist_1.linear.x=clockwise[0]
            self.twist_1.linear.y=clockwise[1]
            self.twist_1.linear.z=clockwise[2]
        if num==1:
            self.twist_1.linear.x=anticlockwise[0]
            self.twist_1.linear.y=anticlockwise[1]
            self.twist_1.linear.z=anticlockwise[2]
        if num==2:
            self.twist_1.linear.x=90.0
            self.twist_1.linear.y=90.0
            self.twist_1.linear.z=90.0




def main(args=None):

    rclpy.init(args=args)
    
    # Create an instance of the HBController class
    hb_controller = HBControl()
   
    global i,pen_down
    # Main loop
    while rclpy.ok():
        # Check if the service call is done
        if hb_controller.bot_x_goal == []  and hb_controller.bot_x_goal == []:
            pass
        else:
            #########           GOAL POSE             #########
            x_goal= hb_controller.bot_x_goal[i]
            y_goal= hb_controller.bot_y_goal[i]
            # theta_goal= hb_controller.bot_theta_goal
            ####################################################
            phi=math.arctan2((y_goal-hb_controller.bot_y)/(x_goal-hb_controller.bot_x))
            x_error=x_goal-hb_controller.bot_x
            y_error=y_goal-hb_controller.bot_y
            distance=((x_error)**2+(y_error)**2)**0.5
            if abs(math.pi/2-(phi-hb_controller.bot_theta))>=0.1:
                if phi-hb_controller.bot_theta<0:
                    hb_controller.rotate(0)
                else : 
                    hb_controller.rotate(1)
            if abs(math.pi/2-(phi-hb_controller.bot_theta))<0.1:       
                hb_controller.rotate(2)
                if distance>=distance_threshold:
                    hb_controller.moveforward(True)
                if distance<distance_threshold:
                    hb_controller.moveforward(False) 
                    hb_controller.pen1.data=True 
            
            hb_controller.pub_1.publish(hb_controller.twist_1)
            hb_controller.pen_pub1.publish(hb_controller.pen1)

                

           
            if distance < distance_threshold :
                i = i+1
            if i==len(hb_controller.bot_x_goal):
                hb_controller.twist_1.linear.x=90.0
                hb_controller.twist_1.linear.y=90.0
                hb_controller.twist_1.linear.z=90.0
                hb_controller.pen1.data=False
                hb_controller.pub_1.publish(hb_controller.twist_1)
                hb_controller.pen_pub1.publish(hb_controller.pen1)

                break     
                ####################################################
        # hb_controller.get_logger().info("GOAL: no ")
        # Spin once to process callbacks
        rclpy.spin_once(hb_controller)
    
    # Destroy the node and shut down ROS
    hb_controller.destroy_node()
    rclpy.shutdown()






if __name__ == '__main__':
    main()    
