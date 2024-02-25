import rclpy
from rclpy.node import Node
import math
import numpy as np
from std_msgs.msg import Bool
from my_robot_interfaces.msg import Goal   
from geometry_msgs.msg import Pose2D


# start1=Bool()
# start2=Bool()
# start3=Bool()


# start1.data=False
# start2.data=True
# start3.data=True
dist_thres=7.0

class ControlFlag(Node):
    def __init__(self):
        super().__init__('controlflag')
        self.buffer=10
        self.bot1_x_goal = []
        self.bot1_y_goal = []
        self.bot2_x_goal = []
        self.bot2_y_goal = []
        self.bot3_x_goal = []
        self.bot3_y_goal = []
        # self.bot_3_theta_goal = 0.0

        self.bot1_x = 0.0
        self.bot1_y = 0.0
        self.bot2_x = 0.0
        self.bot2_y = 0.0
        self.bot3_x = 0.0
        self.bot3_y = 0.0
        

        self.startrunControl = self.create_publisher(Bool, "/startrun", self.buffer)
        self.bot1_pos = self.create_subscription(Pose2D, "/pen1_pose", self.Callback1, 10)
        self.bot2_pos = self.create_subscription(Pose2D, "/pen2_pose", self.Callback2, 10)
        self.bot3_pos = self.create_subscription(Pose2D, "/pen3_pose", self.Callback3, 10)


        self.bot1_goal=self.create_subscription(Goal,'hb_bot_1/goal', self.goalCallBack1, 10)
        self.bot2_goal=self.create_subscription(Goal,'hb_bot_2/goal', self.goalCallBack2, 10)
        self.bot3_goal=self.create_subscription(Goal,'hb_bot_3/goal', self.goalCallBack3, 10)


        self.startrun=Bool()
        self.startrun.data=False

        # self.subscription_bot1 = self.create_subscription(Bool,'hb_bot_1/startpt', self.startCallBack1, self.buffer) 

        # self.subscription_bot2 = self.create_subscription(Bool,'hb_bot_2/startpt', self.startCallBack2, self.buffer) 


        # self.subscription_bot3 = self.create_subscription(Bool,'hb_bot_3/startpt', self.startCallBack3, self.buffer) 
        self.rate = self.create_rate(100)
    def Callback1(self, msg):
        self.bot1_x = msg.x
        self.bot1_y = msg.y

    def Callback2(self, msg):
        self.bot2_x = msg.x
        self.bot2_y = msg.y

    def Callback3(self, msg):
        self.bot3_x = msg.x
        self.bot3_y = msg.y

    def goalCallBack1(self, msg1):
        self.bot1_x_goal = msg1.x
        self.bot1_y_goal = msg1.y
        # self.bot_theta_goal = msg1.theta
    def goalCallBack2(self, msg1):
        self.bot2_x_goal = msg1.x
        self.bot2_y_goal = msg1.y
        # self.bot_theta_goal = msg1.theta
    def goalCallBack3(self, msg1):
        self.bot3_x_goal = msg1.x
        self.bot3_y_goal = msg1.y
        # self.bot_theta_goal = msg1.theta

    def distance_from_1st(self, x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5    # def startCallBack1(self,msg):
        # global start1
        # start1.data=msg.data
        # if start1==True:
            # self.get_logger().info(f'bot1 true')
    # def startCallBack2(self,msg):
    #     global start2
    #     start2.data=msg.data
    #     # start2.data=True
    # #     # if start2==True:
    # #         # self.get_logger().info(f'bot2 true')
    # def startCallBack3(self,msg):
    #     global start3
    #     start3.data=msg.data 
    #     start3.data=True
    #     # if start3==True:
    #         # self.get_logger().info(f'bot3 true')       

def main(args=None):

    rclpy.init(args=args)
    startControl=ControlFlag()
    global dist_thres
    while rclpy.ok():
        if (startControl.bot1_x_goal == []  and startControl.bot1_y_goal == []) or (startControl.bot2_x_goal == []  and startControl.bot2_y_goal == []) or (startControl.bot3_x_goal == []  and startControl.bot3_y_goal == []):
            pass
        else:
            dist1 = startControl.distance_from_1st(startControl.bot1_x_goal[0], startControl.bot1_y_goal[0], startControl.bot1_x, startControl.bot1_y)
            # global start1,start2,start3
            dist2 = startControl.distance_from_1st(startControl.bot2_x_goal[0], startControl.bot2_y_goal[0], startControl.bot2_x, startControl.bot2_y)
            # global start1,start2,start3
            dist3 = startControl.distance_from_1st(startControl.bot3_x_goal[0], startControl.bot3_y_goal[0], startControl.bot3_x, startControl.bot3_y)
            # global start1,start2,start3
            # if start1.data==True and start2.data==True and start3.data==True:
            #     startControl.startrun.data=True
            # startControl.get_logger().info(f'bot1 : {start1}')
            # startControl.get_logger().info(f'bot2 : {start2}')
            # startControl.get_logger().info(f'bot3 : {start3}')
                
            # if start1.data==False or start2.data==False or start3.data==False:
            #     startControl.startrun.data=False   

            # startControl.startrunControl.publish(startControl.startrun)
            # startControl.get_logger().info(f'bot1:{dist1}  bot2:{dist2}  bot3:{dist3}')
            if dist1<dist_thres+10 and dist2<dist_thres+10 and dist3<dist_thres+10:
                startControl.startrun.data = True
            # startControl.startrun.data = True    
            startControl.startrunControl.publish(startControl.startrun)












        rclpy.spin_once(startControl)
    
    # Destroy the node and shut down ROS
    startControl.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()    