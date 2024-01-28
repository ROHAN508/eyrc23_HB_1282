import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
# import _wheel_vel as WheelVel
import tkinter as tk
from tkinter import ttk
from std_msgs.msg import Bool

i=0

# vel_fr_tri=[[20.0,180.0,90.0],[180.0,90.0,28.0],[90.0,0.0,165.0]]
# vel_fr_square=[[25.0,180.0,90.0],[120.0,115.0,20.0],[175.0,17.0,90.0],[64.0,75.0,168.0]]
r=1.9
vel_fr_tri=[[180.0,180.0,180.0],[180.0,180.0,180.0],[180.0,180.0,180.0]]
vel_fr_square=[[180.0,180.0,180.0],[180.0,180.0,180.0],[180.0,180.0,180.0],[180.0,180.0,180.0]]

class Publisher(Node):
    def __init__(self):
        super().__init__('Publisher_node')
        self.timer = self.create_timer(0.2, self.timer_callback)
        self.twist_1 =  Twist()
        self.twist_2=   Twist()
        self.twist_3=   Twist()
        self.bool=Bool()
        self.pub_1 = self.create_publisher(Twist, '/cmd_vel/bot2', 10)
        # self.pub_2 = self.create_publisher(Twist, '/cmd_vel/bot2', 10)
        # self.pub_3 = self.create_publisher(Twist, '/cmd_vel/bot3', 10)
        self.penpub = self.create_publisher(Bool, '/pen2_down', 10)
        self.bool.data=False
        # Initialize Twist message with all components set to 0.0
        self.twist_1.linear.x = 90.0
        self.twist_1.linear.y = 90.0
        self.twist_1.linear.z = 90.0
        self.twist_1.angular.x = 0.0
        self.twist_1.angular.y = 0.0
        self.twist_1.angular.z = 90.0

        self.twist_2.linear.x = 90.0
        self.twist_2.linear.y = 90.0
        self.twist_2.linear.z = 90.0
        self.twist_2.angular.x = 0.0
        self.twist_2.angular.y = 0.0
        self.twist_2.angular.z = 0.0

        self.twist_3.linear.x = 90.0
        self.twist_3.linear.y = 90.0
        self.twist_3.linear.z = 90.0
        self.twist_3.angular.x = 0.0
        self.twist_3.angular.y = 0.0
        self.twist_3.angular.z = 0.0
        self.wheel_vel=[]


    def inverse_kinematics(self,xvel, yvel, ang_vel):
        ############ ADD YOUR CODE HERE ############

        # INSTRUCTIONS & HELP : 
        #	-> Use the target velocity you calculated for the robot in previous task, and
        #	Process it further to find what proportions of that effort should be given to 3 individuals wheels !!
        #	Publish the calculated efforts to actuate robot by applying force vectors on provided topics
        ############################################
        # wheel_vel_1= (-0.33*xvel)+(0.58*yvel)+(0.33*ang_vel)
        # wheel_vel_2= (-0.33*xvel)+(-0.58*yvel)+(0.33*ang_vel)
        # wheel_vel_3= (0.66666*xvel)+(0.33333*ang_vel)
        # w1_vel = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (0.866*yvel))
        # w2_vel = (1/r) * ((ang_vel*dc) + (-0.5*xvel) + (-0.866*yvel))
        # w3_vel = (1/r) * ((ang_vel*dc) + (1*xvel) + (0*yvel))
        wheel_vel_1= (1/r)*(-0.33*xvel)+(0.58*yvel)+(0.04762*ang_vel)
        wheel_vel_2= (1/r)*(-0.33*xvel)+(-0.58*yvel)+(0.04762*ang_vel)
        wheel_vel_3= (1/r)*(0.66666*xvel)+(0.04762*ang_vel)
        return [wheel_vel_1, wheel_vel_2, wheel_vel_3]
    

    def timer_callback(self):
        global i
        
        # if i<35:
        #     self.twist_1.linear.x = vel_fr_tri[0][0]
        #     self.twist_1.linear.y = vel_fr_tri[0][1]
        #     self.twist_1.linear.z = vel_fr_tri[0][2]
        #     self.twist_3.linear.x = vel_fr_square[0][0]
        #     self.twist_3.linear.y = vel_fr_square[0][1]
        #     self.twist_3.linear.z = vel_fr_square[0][2]
        #     # self.twist_2.linear.x = 64.0
        #     # self.twist_2.linear.y = 115.0
        #     # self.twist_2.linear.z = 140.0
        #     self.twist_2.linear.x = 180.0
        #     self.twist_2.linear.y = 180.0
        #     self.twist_2.linear.z = 180.0
        # if i>=35 and i<70:
        #     self.twist_1.linear.x = vel_fr_tri[1][0]
        #     self.twist_1.linear.y = vel_fr_tri[1][1]
        #     self.twist_1.linear.z = vel_fr_tri[1][2]
        #     self.twist_3.linear.x = vel_fr_square[1][0]
        #     self.twist_3.linear.y = vel_fr_square[1][1]
        #     self.twist_3.linear.z = vel_fr_square[1][2]
        # if i>=70 and i<105 :
        #     self.twist_1.linear.x = vel_fr_tri[2][0]
        #     self.twist_1.linear.y = vel_fr_tri[2][1]
        #     self.twist_1.linear.z = vel_fr_tri[2][2]
        #     self.twist_3.linear.x = vel_fr_square[2][0]
        #     self.twist_3.linear.y = vel_fr_square[2][1]
        #     self.twist_3.linear.z = vel_fr_square[2][2]
        # if i>=105 and i<140:
        #     self.twist_1.linear.x = 90.0
        #     self.twist_1.linear.y = 90.0
        #     self.twist_1.linear.z = 90.0
        #     self.twist_3.linear.x = vel_fr_square[3][0]
        #     self.twist_3.linear.y = vel_fr_square[3][1]
        #     self.twist_3.linear.z = vel_fr_square[3][2]
        # if i>=140:
        #     self.twist_3.linear.x = 90.0
        #     self.twist_3.linear.y = 90.0
        #     self.twist_3.linear.z = 90.0 
        #     self.twist_2.linear.x = 90.0
        #     self.twist_2.linear.y = 90.0
        #     self.twist_2.linear.z = 90.0   

            
        # Publish the Twist message
        # self.pub_1.publish(self.twist_1)
        # self.pub_2.publish(self.twist_2)
        # self.pub_3.publish(self.twist_3)
        # i+=1
        


class GuiApp:
    def __init__(self, root, publisher_node):
        self.root = root
        self.root.title("Twist Message GUI")

        # Linear x entry
        ttk.Label(root, text="wheel_1_right:").pack()
        self.linear_x_var = tk.StringVar(value="90.0")
        ttk.Entry(root, textvariable=self.linear_x_var).pack()

        # Linear y entry
        ttk.Label(root, text="wheel_2_left:").pack()
        self.linear_y_var = tk.StringVar(value="90.0")
        ttk.Entry(root, textvariable=self.linear_y_var).pack()

        # Angular z entry
        ttk.Label(root, text="wheel_3_rear:").pack()
        self.angular_z_var = tk.StringVar(value="90.0")
        ttk.Entry(root, textvariable=self.angular_z_var).pack()

        # Buttons
        ttk.Button(root, text="Update", command=self.update_twist).pack()
        ttk.Button(root, text="Stop", command=self.stop_twist).pack()

        # Checkbutton for Bool message
        ttk.Label(root, text="Pen Down:").pack()
        self.pen_down_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(root, variable=self.pen_down_var, text="Down", command=self.update_bool).pack()

        self.publisher_node = publisher_node
        


    def update_twist(self):

        
        # Update the Twist message with new values
        linear_x = float(self.linear_x_var.get())
        linear_y = float(self.linear_y_var.get())
        angular_z = float(self.angular_z_var.get())

        self.publisher_node.twist_1.linear.x = linear_x
        self.publisher_node.twist_1.linear.y = linear_y
        self.publisher_node.twist_1.linear.z = angular_z
        # self.publisher_node.wheel_vel=self.publisher_node.inverse_kinematics(linear_x,linear_y,angular_z)
        # self.publisher_node.get_logger().info(f'wheel_vels:  {self.publisher_node.wheel_vel}')

        # Publish the updated Twist message
        self.publisher_node.pub_1.publish(self.publisher_node.twist_1)

    def stop_twist(self):
        # Set all linear and angular components of the Twist message to 0
        self.publisher_node.twist_1.linear.x = 90.0
        # self.publisher_node.twist_1.linear.x = 0.0
        self.publisher_node.twist_1.linear.y = 90.0
        self.publisher_node.twist_1.linear.z = 90.0
        # self.publisher_node.wheel_vel=self.publisher_node.inverse_kinematics(0,0,0)
        # self.publisher_node.get_logger().info(f'wheel_vels:  {self.publisher_node.wheel_vel}')
        # Publish the stopped Twist message
        self.publisher_node.pub_1.publish(self.publisher_node.twist_1)
    def update_bool(self):
        # Update the Bool message with the value from Checkbutton
        self.publisher_node.bool.data = self.pen_down_var.get()

        # Publish the updated Bool message
        self.publisher_node.penpub.publish(self.publisher_node.bool)


def main(args=None):
    rclpy.init(args=args)
    publisher_node = Publisher()

    # Create a Tkinter GUI
    root = tk.Tk()
    gui_app = GuiApp(root, publisher_node)

    # Run the Tkinter main loop in a separate thread
    root.mainloop()
    rclpy.spin(publisher_node)
    publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
