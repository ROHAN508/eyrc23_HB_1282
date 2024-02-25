import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_srvs.srv import Empty

bot_1 = Bool()
bot_2 = Bool()
bot_3 = Bool()

bot_1.data = False
bot_2.data = False
bot_3.data = False


class stop_bot(Node):
    def __init__(self):
        super().__init__("stop_bot_node")

        self.sub1 = self.create_subscription(Bool, "/stop_bot1", self.callback1, 10)
        self.sub2 = self.create_subscription(Bool, "/stop_bot2", self.callback2, 10)
        self.sub3 = self.create_subscription(Bool, "/stop_bot3", self.callback3, 10)

        


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

class stop_serv(Node):
    def __init__(self):
        super().__init__("StopServiceNode")

        self.client = self.create_client(Empty,"/Stop_Flag")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service 'Stop_Flag' not available, waiting...")

    def stop_func(self):
        req = Empty.Request()
        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info("Run complete :) " + future.result().name)
        else:
            self.get_logger().error("Failed to stop :(")



def main():
    rclpy.init()
    StopBot = stop_bot()
    while True:
        rclpy.spin_once(StopBot)
        StopBot.get_logger().info(f'bot:{bot_1.data} bot2:{bot_2.data} bot3: {bot_3.data}')
        if bot_1.data == True and bot_2.data == True and bot_3.data == True:
            break
    
    StopBot.destroy_node()

    StopServ = stop_serv()
    StopServ.stop_func()

    rclpy.shutdown()

if __name__ == "__main__":
    main()
          
    


