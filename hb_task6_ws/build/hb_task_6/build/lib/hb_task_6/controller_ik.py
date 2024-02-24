import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Wrench
from nav_msgs.msg import Odometry
import time
import math
import numpy as np
from std_msgs.msg import Bool
# from tf_transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from my_robot_interfaces.msg import Goal   
from std_msgs.msg import Float64MultiArray          


pen_down=False
distance_threshold=5
angle_threshold=0.1
forward_vel=[25.0,180.0,90.0]
# forward_vel=[0.0,170.0,90.0]
anticlockwise=[70.0,70.0,70.0]
clockwise=[110.0,110.0,110.0]
i=0
r=1.9
# dc=0.1
dc=5.0


class HBControl(Node):
    def __init__(self):
        super().__init__('hb_controller')
        # self.timer = self.create_timer(0.05, self.timer_callback)
        

        # Initialise the required variables
        self.bot_x_goal = []
        self.bot_y_goal = []
        # self.bot_3_theta_goal = 0.0

        self.bot_x = 0.0
        self.bot_y = 0.0
        self.bot_theta = 0.0
        self.p=1
        self.q=1
        

        self.subscription_bot3 = self.create_subscription(Goal,'hb_bot_1/goal', self.goalCallBack1, 10) 
        

        self.sub_bot_1 = self.create_subscription(Pose2D, "/pen1_pose", self.Callback1, 10)
        self.twist_1 =  Float64MultiArray()
        
        self.stop_pub_1 = self.create_publisher(Bool, "/stop_bot1", 10)
        self.stop_bot = Bool()
        self.stop_bot.data = False
        
        # self.twist_1.linear.x=90.0
        # self.twist_1.linear.y=90.0
        # self.twist_1.linear.z=90.0
        # self.twist_1.angular.z=90.0
        self.twist_1.data = [0.0, 0.0, 0.0]

        self.pub_1 = self.create_publisher(Float64MultiArray, '/map', 10)
        self.pen_pub1 = self.create_publisher(Bool, '/pen1_down', 10)
        self.pen1=Bool()
        self.pen1.data=False

        self.rate = self.create_rate(100)
    
    def Callback1(self, msg):
        self.bot_x = msg.x
        self.bot_y = msg.y
        self.bot_theta = msg.theta
    def goalCallBack1(self, msg1):
        self.bot_x_goal = msg1.x
        self.bot_y_goal = msg1.y
        self.bot_theta_goal = msg1.theta


    def errors(self,x_goal,y_goal,theta_goal):
        h=self.bot_x
        k=self.bot_y
        q=self.bot_theta

        # transformations with respect to the bot frame.
        x_b= (x_goal-h)*(math.cos(q))+(y_goal-k)*(math.sin(q)) #error in x value
        y_b= (h-x_goal)*(math.sin(q))-(math.cos(q))*(k-y_goal) #error in y value
        q_b= (q-theta_goal)*(-1) #error in theta value
        # angle=math.atan2(y_b,x_b)
        distance= ((x_b)**2 + (y_b)**2)**(0.5) #distance of bot from goal pose
        return [x_b,y_b,distance,q_b]        

    
    # def timer_callback(self): 

    #     self.pub_1.publish(self.twist_1)
    #     self.pen_pub1.publish(self.pen1)
    def inverse_kinematics(self,xvel, yvel, ang_vel):
        ## fun mode
        # wheel_vel_1= (-0.33*xvel)+(0.58*yvel)+(0.33*ang_vel)
        # wheel_vel_2= (-0.33*xvel)+(-0.58*yvel)+(0.33*ang_vel)
        # wheel_vel_3= (0.66666*xvel)+(0.33333*ang_vel)
        ##
        wheel_vel_1 = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (0.866*yvel))
        wheel_vel_2 = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (-0.866*yvel))
        wheel_vel_3 = (1/r) * ((ang_vel*dc) + (1*xvel) + (0*yvel))
        # wheel_vel_1= (1/r)*(-0.33*xvel)+(0.58*yvel)+(0.04762*ang_vel)
        # wheel_vel_2= (1/r)*(-0.33*xvel)+(-0.58*yvel)+(0.04762*ang_vel)
        # wheel_vel_3= (1/r)*(0.66666*xvel)+(0.04762*ang_vel)
        return [wheel_vel_1, wheel_vel_2, wheel_vel_3]    
    def pController(self,xError,yError,qError):

        xControl=xError*self.p
        yControl=yError*self.p
        qControl=qError*self.q



        return xControl,yControl,qControl





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
            
            x_bot,y_bot,distance,q_error=hb_controller.errors(x_goal,y_goal,0)
            controlX,controlY,controlQ=hb_controller.pController(x_bot,y_bot,q_error)
            w1_vel,w2_vel,w3_vel=hb_controller.inverse_kinematics(controlX,controlY,controlQ)
            # w1_vel,w2_vel,w3_vel=hb_controller.inverse_kinematics(100,0.0,controlQ)



            hb_controller.twist_1.data[0]=w1_vel
            hb_controller.twist_1.data[1]=w2_vel
            hb_controller.twist_1.data[2]=w3_vel
            hb_controller.pub_1.publish(hb_controller.twist_1)




                    
            
            

                

           
            if distance < distance_threshold :
                hb_controller.pen1.data=True
                i = i+1
                hb_controller.pen_pub1.publish(hb_controller.pen1)
            if i==len(hb_controller.bot_x_goal):
                hb_controller.twist_1.data[0]=0.0
                hb_controller.twist_1.data[1]=0.0
                hb_controller.twist_1.data[2]=0.0
                hb_controller.pen1.data=False
                hb_controller.stop_bot.data=True
                hb_controller.pub_1.publish(hb_controller.twist_1)
                hb_controller.pen_pub1.publish(hb_controller.pen1)
                hb_controller.stop_pub_1.publish(hb_controller.stop_bot)

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