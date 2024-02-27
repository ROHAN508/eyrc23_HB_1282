# ```
# * Team Id : HB#1282
# * Author List : AKSHAR DASH, ROHAN MOHAPATRA
# * Filename: StopFlagServer
# * Theme: HologlyphBots
# * Global Variables: bot_1,bot_2,bot_3
###########################
## this code basically subscribes to the stop bot topics that the controller publishes to and if all the stop bot flags are 
##true then it invokes the service which stops the evaluator


import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
from std_msgs.msg import Bool

bot_1 = Bool()
bot_2 = Bool()
bot_3 = Bool()

bot_1.data = False
bot_2.data = False
bot_3.data = False


class stop_bot(Node):
    def __init__(self):
        super().__init__("stop_bot_node")
        ##create necessary subscriptions
        self.sub1 = self.create_subscription(Bool, "/stop_bot1", self.callback1, 10)
        self.sub2 = self.create_subscription(Bool, "/stop_bot2", self.callback2, 10)
        self.sub3 = self.create_subscription(Bool, "/stop_bot3", self.callback3, 10)

        

    ##callbacks for receiving the flags
    def callback1(self, msg):
            global bot_1
            bot_1 = msg
            self.get_logger().info(f"bot1:{bot_1.data}")
        
    def callback2(self, msg):
            global bot_2
            bot_2 = msg
            self.get_logger().info(f"bot2:{bot_2.data}")

    def callback3(self, msg):
            global bot_3
            bot_3 = msg
            self.get_logger().info(f"bot3:{bot_3.data}")

class StopBotService(Node):
    def __init__(self):
        super().__init__('stop_bot_service')
        self.srv = self.create_service(Empty, '/Stop_Flag', self.stop_callback)

    def stop_callback(self, request, response):
        # Set the global boolean values to True
        

        self.get_logger().info("Bots stopped.")
        return response


def main():
    rclpy.init()


    StopBot = stop_bot()
    while True:
        ##when all flags are raised, it breaks out of this loop and the node is destroyed
        if bot_1.data == True and bot_2.data == True and bot_3.data == True:
            break
        
        rclpy.spin_once(StopBot) 

    StopBot.destroy_node()
    ##creating instance of the service used to stop the evaluator
    stop_bot_service = StopBotService()
    rclpy.spin(stop_bot_service)
    stop_bot_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
