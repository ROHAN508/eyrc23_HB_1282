import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Publisher(Node):
    def __init__(self):
        super().__init__('Publisher_node')
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.twist = Twist()
        self.pub = self.create_publisher(Twist, '/cmd_vel/bot1', 10)

    def timer_callback(self):
        # Set linear and angular velocities
        self.twist.linear.x = 100.0  # Adjust linear velocity as needed
        self.twist.angular.z = 0.0  # Adjust angular velocity as needed

        # Publish the Twist message
        self.pub.publish(self.twist)
        self.get_logger().info(f'Published Twist: Linear={self.twist.linear.x}, Angular={self.twist.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    publisher_node = Publisher()
    rclpy.spin(publisher_node)
    publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
