
# ```
# * Team Id : HB#1282
# * Author List : AKSHAR DASH, ROHAN MOHAPATRA
# * Filename: startpointflag
# * Theme: HologlyphBots
# * Global Variables: dist_thres
###########################

##this code basically subscribes to the goals in function mode and the bot poses to determine the realtive location
##to the starting point of the contour .. if they are close it set a flag to true which tells the controllers to start the drawing
##doing this helps us save time in the evaluator
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from my_robot_interfaces.msg import Goal   
from geometry_msgs.msg import Pose2D

##dist_threshold to check if bots have reached their first point or not
dist_thres=7.0

class ControlFlag(Node):
    def __init__(self):
        super().__init__('controlflag')
        self.buffer=10

        ###initialisation of goal variables
        self.bot1_x_goal = []
        self.bot1_y_goal = []
        self.bot2_x_goal = []
        self.bot2_y_goal = []
        self.bot3_x_goal = []
        self.bot3_y_goal = []
        

        self.bot1_x = 0.0
        self.bot1_y = 0.0
        self.bot2_x = 0.0
        self.bot2_y = 0.0
        self.bot3_x = 0.0
        self.bot3_y = 0.0
        
        ##create necessary subscribers and publishers
        self.startrunControl = self.create_publisher(Bool, "/startrun", self.buffer)
        self.bot1_pos = self.create_subscription(Pose2D, "/pen1_pose", self.Callback1, 10)
        self.bot2_pos = self.create_subscription(Pose2D, "/pen2_pose", self.Callback2, 10)
        self.bot3_pos = self.create_subscription(Pose2D, "/pen3_pose", self.Callback3, 10)


        self.bot1_goal=self.create_subscription(Goal,'hb_bot_1/goal', self.goalCallBack1, 10)
        self.bot2_goal=self.create_subscription(Goal,'hb_bot_2/goal', self.goalCallBack2, 10)
        self.bot3_goal=self.create_subscription(Goal,'hb_bot_3/goal', self.goalCallBack3, 10)


        self.startrun=Bool()
        self.startrun.data=False

    
        self.rate = self.create_rate(100)


    ##callbacks for getting the poses of the bots    
    def Callback1(self, msg):
        self.bot1_x = msg.x
        self.bot1_y = msg.y

    def Callback2(self, msg):
        self.bot2_x = msg.x
        self.bot2_y = msg.y

    def Callback3(self, msg):
        self.bot3_x = msg.x
        self.bot3_y = msg.y
    ##callbacks for getting the goal poses of the bots    

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

    ##gives the distance of the bot from its starting coordinate
    def distance_from_1st(self, x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5    
             

def main(args=None):

    rclpy.init(args=args)
    startControl=ControlFlag()
    global dist_thres
    while rclpy.ok():
        if (startControl.bot1_x_goal == []  and startControl.bot1_y_goal == []) or (startControl.bot2_x_goal == []  and startControl.bot2_y_goal == []) or (startControl.bot3_x_goal == []  and startControl.bot3_y_goal == []):
            pass
        else:
            dist1 = startControl.distance_from_1st(startControl.bot1_x_goal[0], startControl.bot1_y_goal[0], startControl.bot1_x, startControl.bot1_y)
            
            dist2 = startControl.distance_from_1st(startControl.bot2_x_goal[0], startControl.bot2_y_goal[0], startControl.bot2_x, startControl.bot2_y)
            
            dist3 = startControl.distance_from_1st(startControl.bot3_x_goal[0], startControl.bot3_y_goal[0], startControl.bot3_x, startControl.bot3_y)
            
            ##if the bot is near its goal points the startrun flag is set to true and bots pen down and start their run
            
            if dist1<dist_thres+10 and dist2<dist_thres+10 and dist3<dist_thres+10:
                startControl.startrun.data = True
               
            startControl.startrunControl.publish(startControl.startrun)












        rclpy.spin_once(startControl)
    
    # Destroy the node and shut down ROS
    startControl.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()    