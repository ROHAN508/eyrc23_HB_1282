########################################################################################################################
########################################## eYRC 23-24 Hologlyph Bots Task 1A ###########################################
# Team ID: 1282
# Team Leader Name: AKSHAR DASH
# Team Members Name: ROHAN MOHAPATRA, AKSHAR DASH, CH PREMSAI PATRO, ANUP KUMAR NAYAK
# College: NIT ROURKELA
########################################################################################################################

#!/usr/bin/env python3

# Import necessary libraries and modules
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
import math

# Initialize global variables
total_angle1 = 0
total_angle2 = 0
x = None
y = None

# Define the TurtleSnowMan1 class
class TurtleSnowMan1(Node):
    def __init__(self):
        super().__init__("turtle_snow_man1") #intializing node turtle_snow_man1
        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.sub = self.create_subscription(Pose, "/turtle1/pose", self.callback_1, 10)
        self.get_logger().info("TurtleSnowMan1 Node has been started...")
        self.twist = Twist()
        self.twist.linear.x = 1.0  # Linear speed
        self.twist.angular.z = 1.0  # Angular speed

        self.start_angle = None
        self.start_x = None
        self.start_y = None
        self.prev_angle = 0.0

    # Define the callback function for TurtleSnowMan1
    def callback_1(self, pos: Pose):
        global x, y
        global total_angle1
        if self.start_angle is None:
            self.start_angle = pos.theta
            self.start_x = pos.x
            self.start_y = pos.y
            x = pos.x
            y = pos.y

        current_angle = pos.theta

        # Calculate the difference in angles
        if pos.theta >= 0:
            delta_angle = abs(current_angle - self.prev_angle)
            total_angle1 += delta_angle
            self.prev_angle = current_angle

        if pos.theta < 0:
            delta_angle = abs((current_angle + math.pi) - (self.prev_angle - math.pi))
            total_angle1 += delta_angle
            self.prev_angle = 2 * math.pi + current_angle

        # If the turtle has completed one full rotation, stop it
        if total_angle1 >= 2 * math.pi:
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.destroy_node()
        self.get_logger().info(f'theta = {current_angle}')
        self.pub.publish(self.twist)

# Define the TurtleSpawnerNode class
class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("spawn_turtle")#intializing node spawn_turtle

        self.client = self.create_client(Spawn, "spawn")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service 'spawn' not available, waiting...")

    # Define a function to spawn a turtle
    def spawn_turtle(self, x, y, theta, name):
        req = Spawn.Request()
        req.x = x
        req.y = y
        req.theta = theta
        req.name = name

        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info("Spawned a turtle named " + future.result().name)
        else:
            self.get_logger().error("Failed to spawn.")

# Define the TurtleSnowMan2 class
class TurtleSnowMan2(Node):
    def __init__(self):
        super().__init__("turtle_snow_man2")#intializing node turtle_snow_man2
        self.pub = self.create_publisher(Twist, "/turtle2/cmd_vel", 10)
        self.sub = self.create_subscription(Pose, "/turtle2/pose", self.callback_1, 10)
        self.get_logger().info("TurtleSnowMan2 Node has been started...")
        self.twist = Twist()
        self.twist.linear.x = 1.0  # Linear speed
        self.twist.angular.z = -0.5  # Angular speed

        self.start_angle = None
        self.start_x = None
        self.start_y = None
        self.prev_angle = 0.0

    # Define the callback function for TurtleSnowMan2
    def callback_1(self, pos: Pose):
        global total_angle2
        if self.start_angle is None:
            self.start_angle = pos.theta
            self.start_x = pos.x
            self.start_y = pos.y

        current_angle = pos.theta

        # Calculate the difference in angles
        if pos.theta > 0:
            delta_angle = abs(current_angle + self.prev_angle - 2 * math.pi)
            total_angle2 += delta_angle
            self.prev_angle = 2 * math.pi - current_angle

        if pos.theta <= 0:
            delta_angle = abs(self.prev_angle + current_angle)
            total_angle2 += delta_angle
            self.prev_angle = -current_angle

        # If the turtle has completed one full rotation, stop it
        if total_angle2 >= 2 * math.pi:
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.destroy_node()
        self.get_logger().info(f'theta = {current_angle}')
        self.pub.publish(self.twist)

# Define the main function
def main():
    rclpy.init() #intializing ROS
    turtle_snow_man1 = TurtleSnowMan1() 
    try:
        rclpy.spin(turtle_snow_man1)
    except:
        turtle_spawner = TurtleSpawnerNode()
        # Spawn second turtle
        turtle_spawner.spawn_turtle(x, y, 0.0, "turtle2")

    turtle_snow_man2 = TurtleSnowMan2()
    try:
        rclpy.spin(turtle_snow_man2)
    except:
        pass

    rclpy.shutdown()

if __name__ == "__main__":
    main()
