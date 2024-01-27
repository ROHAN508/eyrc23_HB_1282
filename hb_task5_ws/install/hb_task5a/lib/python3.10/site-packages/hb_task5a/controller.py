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
from my_robot_interfaces.msg import Goal             


pen_down=False
distance_threshold=5
angle_threshold=0.1
forward_vel=[25.0,180.0,90.0]
# forward_vel=[0.0,170.0,90.0]
anticlockwise=[70.0,70.0,70.0]
clockwise=[110.0,110.0,110.0]
i=0
class HBControl(Node):
    def __init__(self):
        super().__init__('hb_controller')
        self.timer = self.create_timer(0.05, self.timer_callback)
        

        # Initialise the required variables
        self.bot_x_goal = []
        self.bot_y_goal = []
        # self.bot_3_theta_goal = 0.0

        self.bot_x = 0.0
        self.bot_y = 0.0
        self.bot_theta = 0.0

        

        self.subscription_bot3 = self.create_subscription(Goal,'hb_bot_1/goal', self.goalCallBack1, 10) 
        

        self.sub_bot_1 = self.create_subscription(Pose2D, "/pen1_pose", self.Callback1, 10)
        self.twist_1 =  Twist()
        self.pen1=Bool()
        self.pen1.data=False
        self.twist_1.linear.x=90.0
        self.twist_1.linear.y=90.0
        self.twist_1.linear.z=90.0
        self.twist_1.angular.z=90.0

        self.pub_1 = self.create_publisher(Twist, '/cmd_vel/bot1', 10)
        self.pen_pub1 = self.create_publisher(Bool, '/pen1_down', 10)

        self.rate = self.create_rate(100)
    
    def Callback1(self, msg):
        self.bot_x = msg.x
        self.bot_y = msg.y
        self.bot_theta = msg.theta
    def goalCallBack1(self, msg1):
        self.bot_x_goal = msg1.x
        self.bot_y_goal = msg1.y
        self.bot_theta_goal = msg1.theta

    def errors(self,x_goal,y_goal):
        h=self.bot_x
        k=self.bot_y
        q=self.bot_theta
        # transformations with respect to the bot frame.
        x_b= (x_goal-h)*(math.cos(q))+(y_goal-k)*(math.sin(q)) #error in x value
        y_b= (h-x_goal)*(math.sin(q))-(math.cos(q))*(k-y_goal) #error in y value
        # q_b= (q-theta_goal)*(-1) #error in theta value
        angle=math.atan2(y_b,x_b)
        distance= ((x_b)**2 + (y_b)**2)**(0.5) #distance of bot from goal pose
        return [x_b,y_b,distance,angle]        

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
    def timer_callback(self): 

        self.pub_1.publish(self.twist_1)
        self.pen_pub1.publish(self.pen1)





def main(args=None):

    rclpy.init(args=args)
    
    # Create an instance of the HBController class
    hb_controller = HBControl()
    # x_golar=250
    # y_golar=250
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
            # x_goal= x_golar
            # y_goal= y_golar
            # theta_goal= hb_controller.bot_theta_goal
            ####################################################
            hb_controller.get_logger().info(f'present_x:{hb_controller.bot_x} present_y={hb_controller.bot_y}')
            hb_controller.get_logger().info(f'xgoal:{x_goal} ygoal={y_goal}')
            
            x_bot,y_bot,distance,angle_bot=hb_controller.errors(x_goal,y_goal)
            hb_controller.get_logger().info(f'error:{abs(angle_bot-(math.pi/2))}')

            # hb_controller.twist_1.angular.z=0.0
            if  abs((angle_bot-(math.pi/2)))>angle_threshold:
                if angle_bot<=(math.pi/2) and angle_bot>=-(math.pi/2):
                    hb_controller.rotate(0)
                else : 
                    hb_controller.rotate(1)
            if abs((angle_bot-(math.pi/2)))<=angle_threshold:       
                hb_controller.rotate(2)
                if distance>=distance_threshold:
                    hb_controller.moveforward(True)
                if distance<distance_threshold:
                    hb_controller.moveforward(False) 
        
                    hb_controller.pen1.data=True 
                    
            
            

                

           
            if distance < distance_threshold :
                hb_controller.twist_1.angular.z=0.0
                i = i+1
            if i==len(hb_controller.bot_x_goal):
                hb_controller.twist_1.linear.x=90.0
                hb_controller.twist_1.linear.y=90.0
                hb_controller.twist_1.linear.z=90.0
                hb_controller.pen1.data=False
                hb_controller.twist_1.angular.z=90.0
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
