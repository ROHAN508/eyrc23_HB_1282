import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from geometry_msgs.msg import Pose2D


class Publisher(Node):
    def __init__(self):
        super().__init__('subs_node')
       # Initialze Publisher with the "/Integer" topic
        self.sub1=self.create_subscription(Pose2D,"/pen1_pose",self.timer_callback,10)
        self.sub2=self.create_subscription(Pose2D,"/pen2_pose",self.timer_callback,10)
        self.sub3=self.create_subscription(Pose2D,"/pen3_pose",self.timer_callback,10)

        # self.timer = self.create_timer(0.5,self.timer_callback)
        self.i = 0
    def timer_callback(self,msg):
        self.get_logger().info(f'hiiiiiiii')
       # Assign the msg variable to i
       # Publish the msg 
       # Increment the i

def main(args = None):
    rclpy.init(args=args)
    Publisher_node = Publisher()
    rclpy.spin(Publisher_node)
    Publisher_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

