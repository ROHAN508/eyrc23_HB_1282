
# ```
# * Team Id : HB#1282
# * Author List : AKSHAR DASH, ROHAN MOHAPATRA
# * Filename: nextGoal_image3
# * Theme: HologlyphBots
# * Global Variables:,msg_bot_2, fullimage2,pen_status_2,list_update_2
###########################
##code for giving image contours to bot3 in image mode



##import necessary modules
import rclpy
from rclpy.node import Node  

from my_robot_interfaces.msg import Goal           


from std_msgs.msg import Bool
from .image_utlis import * ##import functions from image_utlis

spacing=5.0


msg_bot_2 = Goal()
# ##goal drawing order
# fullimage2=[returncontour(15),returncontour(11),returncontour(10),returncontour(5)]
fullimage2=[returncontour(13),returncontour(16),returncontour(17),returncontour(15),returncontour(3),returncontour(5),returncontour(31),
            returncontour(4),returncontour(7)]
pen_status_2=Bool()

##check status of pen 
pen_status_2.data=False

####flag for list update
list_update_2=False

class ServiceNode(Node):

    def __init__(self):
        super().__init__('GOAL_node_img3')
        ##creates publishers and subscribers
        
        self.publish_goal_2 = self.create_publisher(Goal, 'hb_bot_3/goal_img', 10)

        self.run_complete2 = self.create_publisher(Bool, '/pen3_complete', 10)

        self.bot2_complete=Bool()
        self.bot2_complete.data=False

        self.pen_2_status = self.create_subscription(Bool, "/pen3_down", self.checkPenStatus_2, 10)
        

        self.resolution1=1
        self.resolution2=1
        self.resolution3=1
        self.scale=1
        self.timer = self.create_timer(0.5, self.timer_callback)
    ##publishes goal every 0.5 seconds
    def timer_callback(self):
        # self.get_logger().info(f'goal published')
        self.publish_goal_2.publish(msg_bot_2)

        # This function will be called every 1 second (1 Hz)
        
    ##callback to check pen status
    def checkPenStatus_2(self,msg):
        global pen_status_2
        pen_status_2.data=msg.data


def main(args=None):
    rclpy.init(args=args)
    service_node = ServiceNode()
    global msg_bot_2
    
    
    
    

    ##index for accessing image contour
    image_idx=0

    while rclpy.ok():
        # service_node.get_logger().info(f'countour number bot2 :{image_idx}')
        ##if the image index is not at the last index
        if image_idx!=len(fullimage2):
            global list_update_2,pen_status_2
            ##if the pen is up and the list update flag is false then contour is found out and published and index is incremented
            ##list_update flag is set to true
            if pen_status_2.data==False and list_update_2==False:
                msg_bot_2.bot_id = 2
                msg_bot_2.x = []
                msg_bot_2.y = []
                contour=fullimage2[image_idx]
                
                for coordinate in contour:
                    
                    msg_bot_2.x.append(coordinate[0])
                    msg_bot_2.y.append((coordinate[1]-500)*-1)
                service_node.get_logger().info(f'{msg_bot_2.x}')
                            
                msg_bot_2.theta = 0.0
                list_update_2=True
                image_idx+=1  
                service_node.get_logger().info(f'goal created')
                service_node.publish_goal_2.publish(msg_bot_2)
                rclpy.spin_once(service_node)
            # service_node.get_logger().info(msg_bot_2)

            ##if the pen is down and the list update flag is true, then the flag resets
            if pen_status_2.data==True and list_update_2==True:
                list_update_2=False

        
        ##if all contours are done , bot complete flag is raised and published          
        if image_idx==len(fullimage2):
            service_node.bot2_complete.data=True
            service_node.run_complete2.publish(service_node.bot2_complete) 
            service_node.get_logger().info(f'stup {service_node.bot2_complete}')       
        
            
        


        service_node.publish_goal_2.publish(msg_bot_2)
           
           
            

        
        # time.sleep(1)
        rclpy.spin_once(service_node)
    rclpy.shutdown()
        
if __name__ == '__main__':
    main()

#######################################     DO NOT MODIFY THIS  FILE     ##########################################