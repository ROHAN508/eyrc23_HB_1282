# ```
# * Team Id : HB#1282
# * Author List : AKSHAR DASH, ROHAN MOHAPATRA
# * Filename: controller1
# * Theme: HologlyphBots
# * Functions: errors, inverse kinematics,Pcontroller
# * Global Variables: pen_down,distance_threshold,angle_threshold,i,r,dc,prev_msgx,run_complete
###########################

## this code controls the movement of bot1##



import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
import time
import math
import numpy as np
from std_msgs.msg import Bool
from my_robot_interfaces.msg import Goal   
from std_msgs.msg import Float64MultiArray   

pen_down=False ##initialisation of pen status
distance_threshold=5.5## distance to achieve before moving to next goal

angle_threshold=0.1# angular threshold

i=0 ##index for traversing through list of coordinates
r=1.9## radius of individual wheel
dc=0.1## radius of the bot
# dc=5.0



run_complete=Bool()
run_complete.data=False## to check if run is completed


class HBControl(Node):
    ##node for function mode
    def __init__(self):
        super().__init__('hb_controller')
        

        # Initialise the required variables
        self.bot_x_goal = [] #for storing the goal coordinates x
        self.bot_y_goal = [] #for storing the goal coordinates y
        
        self.bot_x = 0.0 #intitialisation of bot position
        self.bot_y = 0.0
        self.bot_theta = 0.0
        ##some scaling parameters
        self.p=1
        self.q=1
        
        ##parameter initialisation which waits
        self.start_bot = False
        ## create the required subscriptions
        
        self.subscription_bot = self.create_subscription(Goal,'hb_bot_1/goal', self.goalCallBack1, 10) 
        self.startrun = self.create_subscription(Bool,"/startrun", self.startCallBack1, 10)

        

        self.sub_bot = self.create_subscription(Pose2D, "/pen1_pose", self.Callback1, 10)
        self.twist_1 =  Float64MultiArray()
        
        self.stop_pub_1 = self.create_publisher(Bool, "/stop_bot1", 10)
        self.stop_bot = Bool()
        self.stop_bot.data = False

        self.twist_1.data = [0.0, 0.0, 0.0]
        

        self.pub_1 = self.create_publisher(Float64MultiArray, '/map', 10)
        self.pen_pub1 = self.create_publisher(Bool, '/pen1_down', 10)
        self.pen1=Bool()
        self.pen1.data=False

        self.rate = self.create_rate(100)

    ##callback function which tells the bot to pendown and start the run
    def startCallBack1(self, msg):
        self.start_bot=msg.data    
    ##callback for getting current bot pose
    def Callback1(self, msg):
        self.bot_x = msg.x
        self.bot_y = (msg.y-500)*-1
        self.bot_theta = msg.theta
    ##callback function for receiving Goals    
    def goalCallBack1(self, msg1):
        self.bot_x_goal = msg1.x
        self.bot_y_goal = msg1.y
        self.bot_theta_goal = msg1.theta

    ##method to calculate the errors in the bot frame and also the distance
    def errors(self,x_goal,y_goal,theta_goal):
        h=self.bot_x
        k=self.bot_y
        q=self.bot_theta

        # transformations with respect to the bot frame.
        x_b= (x_goal-h)*(math.cos(q))+(y_goal-k)*(math.sin(q)) #error in x value
        y_b= (h-x_goal)*(math.sin(q))-(math.cos(q))*(k-y_goal) #error in y value
        q_b= (q-theta_goal)*(-1) #error in theta value
        
        distance= ((x_b)**2 + (y_b)**2)**(0.5) #distance of bot from goal pose
        return [x_b,y_b,distance,q_b]        
    ##method to calculate the inverse kinematics
    def inverse_kinematics(self,xvel, yvel, ang_vel):
        
        wheel_vel_1 = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (0.866*yvel))
        wheel_vel_2 = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (-0.866*yvel))
        wheel_vel_3 = (1/r) * ((ang_vel*dc) + (1*xvel) + (0*yvel))
        
        return [wheel_vel_1, wheel_vel_2, wheel_vel_3]
    ##scaling of the errors if requuired    
    def pController(self,xError,yError,qError):

        xControl=xError*self.p
        yControl=yError*self.p
        qControl=qError*self.q

        return xControl,yControl,qControl
    
class HBControlimg(Node):
    ##node for image mode
    def __init__(self):
        super().__init__('hb_controller')
        

        # Initialise the required variables
        self.bot_x_goal = []#for storing the goal coordinates x
        self.bot_y_goal = []#for storing the goal coordinates y
        #
        #intitialisation of bot position
        self.bot_x = 0.0
        self.bot_y = 0.0
        self.bot_theta = 0.0
        ##some scaling parameters
        self.p=1
        self.q=1
        

        ## creation of publishers and subscribers

        self.subscription_bot3 = self.create_subscription(Goal,'hb_bot_1/goal_img', self.goalCallBack1, 10) 
        self.run_complete=self.create_subscription(Bool,'/pen1_complete',self.completeCallback,10)

        self.sub_bot_1 = self.create_subscription(Pose2D, "/pen1_pose", self.Callback1, 10)
        self.twist_1 =  Float64MultiArray()

        self.stop_pub_2 = self.create_publisher(Bool, "/stop_bot1", 10)
        self.stop_bot = Bool()
        self.stop_bot.data = False
        
        self.twist_1.data = [0.0, 0.0, 0.0]

        self.pub_1 = self.create_publisher(Float64MultiArray, '/map', 10)
        self.pen_pub1 = self.create_publisher(Bool, '/pen1_down', 10)
        self.pen1=Bool()
        self.pen1.data=False

        self.rate = self.create_rate(100)
    ## callback to check if the run is complete or not   
    def completeCallback(self,msg):
        global run_complete
        run_complete.data=msg.data
    ##callback for current position of the bot
    def Callback1(self, msg):
        self.bot_x = msg.x
        self.bot_y = (msg.y-500)*-1
        self.bot_theta = msg.theta

    ##callback for receiving the goals    
    def goalCallBack1(self, msg1):
        self.bot_x_goal = msg1.x
        self.bot_y_goal = msg1.y
        self.bot_theta_goal = msg1.theta
        

    ## method for calculating the errors in botframe
    def errors(self,x_goal,y_goal,theta_goal):
        h=self.bot_x
        k=self.bot_y
        q=self.bot_theta
        # transformations with respect to the bot frame.
        x_b= (x_goal-h)*(math.cos(q))+(y_goal-k)*(math.sin(q)) #error in x value
        y_b= (h-x_goal)*(math.sin(q))-(math.cos(q))*(k-y_goal) #error in y value
        q_b= (q-theta_goal)*(-1) #error in theta value
        
        distance= ((x_b)**2 + (y_b)**2)**(0.5) #distance of bot from goal pose
        return [x_b,y_b,distance,q_b]        

    ## method to calculate the inverse kinematics of the bot
    def inverse_kinematics(self,xvel, yvel, ang_vel):
        
        wheel_vel_1 = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (0.866*yvel))
        wheel_vel_2 = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (-0.866*yvel))
        wheel_vel_3 = (1/r) * ((ang_vel*dc) + (1*xvel) + (0*yvel))
        
        return [wheel_vel_1, wheel_vel_2, wheel_vel_3]   
    ## method to scale the errrors if required 
    def pController(self,xError,yError,qError):

        xControl=xError*self.p
        yControl=yError*self.p
        qControl=qError*self.q

        return xControl,yControl,qControl
    
def main(args=None):
    ##our code first prompts the user to input 0 or 1 which is used to decide if the bot will run in image or function mode
    while True:
        mode=int(input("select mode(0 for funtion , 1 for image):"))
        if mode==0 or mode==1:
            break
        else:
            print('invalid input')
    ##if mode is function
    if mode==0:
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
                
                ####################################################

                ##logger for debugging purposes
                # hb_controller.get_logger().info(f'present_x:{hb_controller.bot_x} present_y={hb_controller.bot_y}')
                # hb_controller.get_logger().info(f'xgoal:{x_goal} ygoal={y_goal}')
                ## calculation of bot distance errors and wheel velocities using the methods
                x_bot,y_bot,distance,q_error=hb_controller.errors(x_goal,y_goal,0)
                controlX,controlY,controlQ=hb_controller.pController(x_bot,y_bot,q_error)
                w1_vel,w2_vel,w3_vel=hb_controller.inverse_kinematics(controlX,controlY,controlQ)
                
                ##in this condition , it is ensured that the bot reaches the first points of its contour using the goal index i 
                if i ==0:
                    hb_controller.twist_1.data[0]=w1_vel
                    hb_controller.twist_1.data[1]=w2_vel
                    hb_controller.twist_1.data[2]=w3_vel

                ##in this condition , the bot has reached the first point of its contour and it waits for other bots to do the same
                if i==1 and hb_controller.start_bot==False:

                    hb_controller.twist_1.data[0]=0.0
                    hb_controller.twist_1.data[1]=0.0
                    hb_controller.twist_1.data[2]=0.0
                ## if the start_bot flag is True , the bots start their run and pen is down
                if i>0 and hb_controller.start_bot==True:    

                    hb_controller.twist_1.data[0]=w1_vel
                    hb_controller.twist_1.data[1]=w2_vel
                    hb_controller.twist_1.data[2]=w3_vel
                    hb_controller.pen1.data=True
                ## publishing for debugging purposes
                # hb_controller.twist_1.data[0]=w1_vel
                # hb_controller.twist_1.data[1]=w2_vel
                # hb_controller.twist_1.data[2]=w3_vel
                hb_controller.pub_1.publish(hb_controller.twist_1)




                        
                
                

                    

                ##if the distance between current and goal coordinate is less than the threshold set, index is incremented
                if distance < distance_threshold :
                    #
                    i = i+1
                    hb_controller.pen_pub1.publish(hb_controller.pen1)
            
                ## if bot reaches the end of the list , pen is up and bot is stopped   
                if i==len(hb_controller.bot_x_goal):
                    hb_controller.twist_1.data[0]=0.0
                    hb_controller.twist_1.data[1]=0.0
                    hb_controller.twist_1.data[2]=0.0
                    hb_controller.pen1.data=False
                    hb_controller.stop_bot.data=True
                    hb_controller.pub_1.publish(hb_controller.twist_1)
                    hb_controller.pen_pub1.publish(hb_controller.pen1)
                    hb_controller.stop_pub_1.publish(hb_controller.stop_bot)
                    hb_controller.get_logger().info( f'bot1 stopped {hb_controller.stop_bot.data}')

                    break     
                    ####################################################
            
            # Spin once to process callbacks
            rclpy.spin_once(hb_controller)
        
        # Destroy the node and shut down ROS
        hb_controller.destroy_node()
        rclpy.shutdown()
    ##image mode
    if mode==1:
        rclpy.init(args=args)
    
        # Create an instance of the HBControlimg class
        hb_controller = HBControlimg()

        # hb_controller.get_logger().info(f'instance created')
        
        global pen_down, run_complete
        i=0
        # Main loop
        while rclpy.ok():
            
            # Check if the service call is done
            if hb_controller.bot_x_goal == []  and hb_controller.bot_y_goal == []:
                ## checks if the node properly receives the goal coordinates or not . if it doesnt , pass is printed
                hb_controller.get_logger().info(f'pass')                
                rclpy.spin_once(hb_controller)
            else:
                #########           GOAL POSE             #########
                x_goal= hb_controller.bot_x_goal[i]
                y_goal= hb_controller.bot_y_goal[i]
                ##logger for debugging purposes
                hb_controller.get_logger().info(f'present_x:{hb_controller.bot_x} present_y={hb_controller.bot_y}')
                hb_controller.get_logger().info(f'xgoal:{x_goal} ygoal={y_goal}')
                ## all  the errors and the wheel velcoities are calculated using the methods 
                x_bot,y_bot,distance,q_error=hb_controller.errors(x_goal,y_goal,0)
                controlX,controlY,controlQ=hb_controller.pController(x_bot,y_bot,q_error)
                w1_vel,w2_vel,w3_vel=hb_controller.inverse_kinematics(controlX,controlY,controlQ)
                

                ## publishing data

                hb_controller.twist_1.data[0]=w1_vel
                hb_controller.twist_1.data[1]=w2_vel
                hb_controller.twist_1.data[2]=w3_vel
                hb_controller.pub_1.publish(hb_controller.twist_1)


                ##checks if distance is less than threshold , goal index is incremented
                if distance < distance_threshold :
                    
                    i = i+1
                ##if goal index is 1 , pen is down   
                if i==1:
                    hb_controller.pen1.data=True
                    hb_controller.pen_pub1.publish(hb_controller.pen1)
                ##if the contour is completed, it asks the goal publisher for the next contour
                if i==len(hb_controller.bot_x_goal):
                    hb_controller.twist_1.data[0]=0.0
                    hb_controller.twist_1.data[1]=0.0
                    hb_controller.twist_1.data[2]=0.0
                    hb_controller.pen1.data=False
                    i=0
                    hb_controller.pub_1.publish(hb_controller.twist_1)
                    hb_controller.pen_pub1.publish(hb_controller.pen1)
                    
                    time.sleep(0.5)
                    hb_controller.get_logger().info(f'{run_complete.data}')
                ## if the goal publisher sets the flag that the run is completed , the loop breaks and code ends
                if run_complete.data==True and i==len(hb_controller.bot_x_goal)-1:
                    hb_controller.twist_1.data[0]=0.0
                    hb_controller.twist_1.data[1]=0.0
                    hb_controller.twist_1.data[2]=0.0
                    hb_controller.stop_bot.data=True
                    hb_controller.pen1.data=False
                    hb_controller.pub_1.publish(hb_controller.twist_1)
                    hb_controller.pen_pub1.publish(hb_controller.pen1)
                    hb_controller.stop_pub_2.publish(hb_controller.stop_bot)

                    break     
                    ####################################################
            
            # Spin once to process callbacks
            rclpy.spin_once(hb_controller)
        
        # Destroy the node and shut down ROS
        hb_controller.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main() 


