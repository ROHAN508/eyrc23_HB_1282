# ```
# * Team Id : HB#1282
# * Author List : AKSHAR DASH, ROHAN MOHAPATRA
# * Filename: mapping3
# * Theme: HologlyphBots
# * Global Variables: max_rpm
###########################


##import required modules



import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import Goal             
from std_msgs.msg import Float64MultiArray

# max_rpm=40
max_rpm=38## variable to store the max rpm that can be asiigned to a individual motor



class mapper(Node):
    def __init__(self):
        super().__init__('mapper3')
        
        self.mapper = self.create_subscription(Float64MultiArray,'/map3', self.mapCallBack1, 10)
        self.interp=self.create_publisher(Float64MultiArray,'/interp3',10)
        self.interpMsg=Float64MultiArray
        # self.w_max=0.0
        

        self.rate = self.create_rate(100)
     ##callback function to subscribe to data from the controller
    ##the max value of wheel velocity gets assigned to the max_rpm and other wheel velocities are scaled accodrding to that value 
    def mapCallBack1(self, msg1):
        global max_rpm
        self.w1=msg1.data[0]
        self.w2=msg1.data[1]
        self.w3=msg1.data[2]

        self.w_max=max(self.w1,self.w2,self.w3)
        if self.w1==0.0 and self.w2==0.0 and self.w3==0.0:

            self.interpMsg = Float64MultiArray()
            self.interpMsg.data = [self.w1, self.w2, self.w3]
            self.interp.publish(self.interpMsg)
        
        else:
            self.r1=self.w1/self.w_max
            self.r2=self.w2/self.w_max
            self.r3=self.w3/self.w_max

            self.w1=max_rpm*self.r1
            self.w2=max_rpm*self.r2
            self.w3=max_rpm*self.r3

            self.interpMsg = Float64MultiArray()
            self.interpMsg.data = [self.w1, self.w2, self.w3]
            self.interp.publish(self.interpMsg)



    
    


def main(args=None):

    rclpy.init(args=args)
    
    # Create an instance of the HBController class
    hb_controller = mapper()

    # Main loop
    while rclpy.ok():
        # Check if the service call is done
        
                ####################################################
        # hb_controller.get_logger().info("GOAL: no ")
        # Spin once to process callbacks
        rclpy.spin_once(hb_controller)
    
    # Destroy the node and shut down ROS
    hb_controller.destroy_node()
    rclpy.shutdown()






if __name__ == '__main__':
    main()    