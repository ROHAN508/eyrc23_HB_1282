import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import tkinter as tk
from tkinter import ttk

class Publisher(Node):
    def __init__(self):
        super().__init__('Publisher_node')
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.twist = Twist()
        self.pub = self.create_publisher(Twist, '/cmd_vel/bot1', 10)

        # Initialize Twist message with all components set to 0.0
        self.twist.linear.x = 0.0
        self.twist.linear.y = 0.0
        self.twist.linear.z = 0.0
        self.twist.angular.x = 0.0
        self.twist.angular.y = 0.0
        self.twist.angular.z = 0.0

    def timer_callback(self):
        # Publish the Twist message
        self.pub.publish(self.twist)
        self.get_logger().info(f'Published Twist: Linear={self.twist.linear}, Angular={self.twist.angular}')

class GuiApp:
    def __init__(self, root, publisher_node):
        self.root = root
        self.root.title("Twist Message GUI")

        # Linear x entry
        ttk.Label(root, text="Linear X:").pack()
        self.linear_x_var = tk.StringVar(value="0.0")
        ttk.Entry(root, textvariable=self.linear_x_var).pack()

        # Linear y entry
        ttk.Label(root, text="Linear Y:").pack()
        self.linear_y_var = tk.StringVar(value="0.0")
        ttk.Entry(root, textvariable=self.linear_y_var).pack()

        # Angular z entry
        ttk.Label(root, text="Angular Z:").pack()
        self.angular_z_var = tk.StringVar(value="0.0")
        ttk.Entry(root, textvariable=self.angular_z_var).pack()

        # Buttons
        ttk.Button(root, text="Update", command=self.update_twist).pack()
        ttk.Button(root, text="Stop", command=self.stop_twist).pack()

        self.publisher_node = publisher_node

    def update_twist(self):
        # Update the Twist message with new values
        linear_x = float(self.linear_x_var.get())
        linear_y = float(self.linear_y_var.get())
        angular_z = float(self.angular_z_var.get())

        self.publisher_node.twist.linear.x = linear_x
        self.publisher_node.twist.linear.y = linear_y
        self.publisher_node.twist.angular.z = angular_z

        # Publish the updated Twist message
        self.publisher_node.pub.publish(self.publisher_node.twist)

    def stop_twist(self):
        # Set all linear and angular components of the Twist message to 0
        self.publisher_node.twist.linear.x = 0.0
        self.publisher_node.twist.linear.y = 0.0
        self.publisher_node.twist.angular.z = 0.0

        # Publish the stopped Twist message
        self.publisher_node.pub.publish(self.publisher_node.twist)

def main(args=None):
    rclpy.init(args=args)
    publisher_node = Publisher()

    # Create a Tkinter GUI
    root = tk.Tk()
    gui_app = GuiApp(root, publisher_node)

    # Run the Tkinter main loop in a separate thread
    root.mainloop()

    publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
