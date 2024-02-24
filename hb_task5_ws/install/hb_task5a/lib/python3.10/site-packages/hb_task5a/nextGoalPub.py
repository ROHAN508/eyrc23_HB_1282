#######################################     DO NOT MODIFY THIS  FILE     ##########################################
import numpy as np
import matplotlib.pyplot as plt
from my_robot_interfaces.srv import NextGoal             
import rclpy
from rclpy.node import Node  
import random
import time
from my_robot_interfaces.msg import Goal           
from my_robot_interfaces.msg import Shape           
import math
from std_msgs.msg import Bool

spacing=5.0
hexagon_points=[[200, 150], [175, 200], [125, 200], [100, 150], [125, 100], [175, 100],[200, 150]]

triangle_points=[[300, 100], [400, 100],[300, 200], [300, 100]]


# rectangle_points= [[200, 300],[250,300],[300,300] ,[350,300],[400, 300],[400,350], [400, 400],[375,400],[350,400],[325,400],[300,400],[275,400],[250,400],[225,400], [200, 400],[200,350], [200, 300]]
rectangle_points= [[200, 300],[250,300],[300,300] ,[350,300],[400, 300],[400,350], [400, 400],[300,400], [200, 400],[200,350], [200, 300]]

contour_1 = [
    [214, 251], [212, 253], [212, 254], [213, 255], [213, 258], [214, 259], [214, 262], [215, 263], 
    [215, 265], [216, 266], [216, 268], [217, 269], [217, 270], [218, 271], [218, 272], [220, 274], 
    [220, 275], [223, 278], [223, 279], [226, 282], [227, 282], [230, 285], [231, 285], [233, 287], 
    [234, 287], [235, 288], [236, 288], [237, 289], [239, 289], [240, 290], [242, 290], [243, 291], 
    [247, 291], [248, 292], [260, 292], [261, 291], [264, 291], [265, 290], [268, 290], [269, 289], 
    [270, 289], [271, 288], [272, 288], [273, 287], [274, 287], [275, 286], [276, 286], [279, 283], 
    [280, 283], [286, 277], [286, 276], [288, 274], [288, 273], [290, 271], [290, 270], [291, 269], 
    [291, 267], [292, 266], [292, 264], [293, 263], [293, 261], [294, 260], [294, 256], [295, 255], 
    [295, 252], [294, 252], [293, 251], [290, 251], [289, 252], [219, 252], [218, 251]
]
contour_2 = [
    [253, 141], [252, 142], [240, 142], [239, 143], [234, 143], [233, 144], [230, 144], [229, 145], [226, 145],
    [225, 146], [223, 146], [222, 147], [221, 147], [220, 148], [218, 148], [217, 149], [216, 149], [215, 150],
    [214, 150], [213, 151], [211, 151], [210, 152], [209, 152], [207, 154], [206, 154], [205, 155], [204, 155],
    [201, 158], [200, 158], [198, 160], [197, 160], [192, 165], [191, 165], [185, 171], [185, 172], [181, 176],
    [181, 177], [178, 180], [178, 181], [176, 183], [176, 184], [174, 186], [174, 187], [173, 188], [173, 189],
    [172, 190], [172, 191], [171, 192], [171, 193], [170, 194], [170, 195], [169, 196], [169, 197], [168, 198],
    [168, 199], [167, 200], [167, 202], [166, 203], [166, 205], [165, 206], [165, 209], [164, 210], [164, 213],
    [163, 214], [163, 218], [162, 219], [162, 247], [163, 248], [163, 252], [164, 253], [164, 257], [165, 258],
    [165, 260], [166, 261], [166, 263], [167, 264], [167, 266], [168, 267], [168, 269], [169, 270], [169, 271],
    [170, 272], [170, 273], [171, 274], [171, 275], [172, 276], [172, 277], [173, 278], [173, 279], [174, 280],
    [174, 281], [176, 283], [176, 284], [179, 287], [179, 288], [182, 291], [182, 292], [195, 305], [196, 305],
    [199, 308], [200, 308], [203, 311], [204, 311], [205, 312], [206, 312], [207, 313], [208, 313], [210, 315],
    [211, 315], [212, 316], [213, 316], [214, 317], [215, 317], [216, 318], [218, 318], [219, 319], [220, 319],
    [221, 320], [223, 320], [224, 321], [226, 321], [227, 322], [230, 322], [231, 323], [234, 323], [235, 324],
    [240, 324], [241, 325], [267, 325], [268, 324], [273, 324], [274, 323], [277, 323], [278, 322], [280, 322],
    [281, 321], [283, 321], [284, 320], [286, 320], [287, 319], [289, 319], [290, 318], [291, 318], [292, 317],
    [293, 317], [294, 316], [295, 316], [296, 315], [297, 315], [298, 314], [299, 314], [300, 313], [301, 313],
    [303, 311], [304, 311], [306, 309], [307, 309], [310, 306], [311, 306], [315, 302], [316, 302], [322, 296],
    [322, 295], [327, 290], [327, 289], [329, 287], [329, 286], [332, 283], [332, 282], [333, 281], [333, 280],
    [334, 279], [334, 278], [335, 277], [335, 276], [336, 275], [336, 274], [337, 273], [337, 272], [338, 271],
    [338, 270], [339, 269], [339, 267], [340, 266], [340, 265], [341, 264], [341, 261], [342, 260], [342, 258],
    [343, 257], [343, 254], [344, 253], [344, 249], [345, 248], [345, 219], [344, 218], [344, 214], [343, 213],
    [343, 210], [342, 209], [342, 206], [341, 205], [341, 203], [340, 202], [340, 200], [339, 199], [339, 198],
    [338, 197], [338, 196], [337, 195], [337, 193], [336, 192], [336, 191], [335, 190], [335, 189], [333, 187],
    [333, 186], [332, 185], [332, 184], [330, 182], [330, 181], [327, 178], [327, 177], [323, 173], [323, 172],
    [314, 163], [313, 163], [309, 159], [308, 159], [306, 157], [305, 157], [303, 155], [302, 155], [301, 154],
    [300, 154], [299, 153], [298, 153], [296, 151], [295, 151], [294, 150], [293, 150], [292, 149], [290, 149],
    [289, 148], [288, 148], [287, 147], [285, 147], [284, 146], [282, 146], [281, 145], [278, 145], [277, 144],
    [274, 144], [273, 143], [269, 143], [268, 142], [259, 142], [258, 141]
]
contour_3 = [
    [226, 191], [225, 192], [224, 192], [222, 194], [222, 195], [221, 196], [221, 197], [220, 198], [220, 202],
    [219, 203], [219, 206], [220, 207], [220, 211], [221, 212], [221, 213], [222, 214], [222, 215], [225, 218],
    [227, 218], [228, 219], [230, 219], [231, 218], [233, 218], [236, 215], [236, 214], [237, 213], [237, 211],
    [238, 210], [238, 199], [237, 198], [237, 197], [236, 196], [236, 195], [232, 191]
]
contour_4 = [
    [275, 190], [274, 191], [273, 191], [270, 194], [270, 195], [269, 196], [269, 197], [268, 198], [268, 209],
    [269, 210], [269, 212], [270, 213], [270, 214], [273, 217], [274, 217], [275, 218], [280, 218], [281, 217],
    [282, 217], [283, 216], [283, 215], [285, 213], [285, 211], [286, 210], [286, 208], [287, 207], [287, 201],
    [286, 200], [286, 198], [285, 197], [285, 195], [283, 193], [283, 192], [282, 192], [280, 190]
]

fullimage=[contour_1,contour_2,contour_3,contour_4]

pen_status_2=Bool()
pen_status_2.data=False
list_update_2=False

class ServiceNode(Node):

    def __init__(self):
        super().__init__('GOAL_node')

        self.publish_goal_1 = self.create_publisher(Goal, 'hb_bot_1/goal', 10)
        self.publish_goal_2 = self.create_publisher(Goal, 'hb_bot_2/goal', 10)
        self.publish_goal_3 = self.create_publisher(Goal, 'hb_bot_3/goal', 10)

        self.run_complete2 = self.create_publisher(Bool, '/pen2_complete', 10)

        self.bot2_complete=Bool()
        self.bot2_complete.data=False

        self.pen_2_status = self.create_subscription(Bool, "/pen3_down", self.checkPenStatus_2, 10)
        
        # self.publish_shape_1  = self.create_publisher(Shape, 'shape_1', 10)
        # self.publish_shape_2  = self.create_publisher(Shape, 'shape_2', 10)
        # self.publish_shape_3  = self.create_publisher(Shape, 'shape_3', 10)
        self.resolution1=1
        self.resolution2=1
        self.resolution3=1
        self.scale=1
    
    def checkPenStatus_2(self,msg):
        global pen_status_2
        pen_status_2.data=msg.data

    def generate_points(self):
        coordinates_list1x = []
        coordinates_list1y = []
        coordinates_list2x = []
        coordinates_list2y = []
        coordinates_list3x = []
        coordinates_list3y = []

        for angle in range(0, 121, self.resolution1):
            t_rad = math.radians(angle)
            # x1 = (200 * math.cos(t_rad)) / self.scale
            # y1 = (150 * math.sin(4 * t_rad)) / self.scale
            x1 = ((200 * math.cos(t_rad)) / self.scale)+250
            y1 = ((150 * math.sin(4 * t_rad)) / self.scale)+250
            coordinates_list1x.append(x1)
            coordinates_list1y.append(y1)

        for angle in range(120, 241, self.resolution2):
            t_rad = math.radians(angle)
            # x2 = (200 * math.cos(t_rad)) / self.scale
            # y2 = (150 * math.sin(4 * t_rad)) / self.scale
            x2 = ((200 * math.cos(t_rad)) / self.scale)+250
            y2 = ((150 * math.sin(4 * t_rad)) / self.scale)+250
            coordinates_list2x.append(x2)
            coordinates_list2y.append(y2)

        for angle in range(240, 361, self.resolution3):
            t_rad = math.radians(angle)
            # x3 = (200 * math.cos(t_rad)) / self.scale
            # y3 = (150 * math.sin(4 * t_rad)) / self.scale
            x3 = ((200 * math.cos(t_rad)) / self.scale)+250
            y3 = ((150 * math.sin(4 * t_rad)) / self.scale)+250
            coordinates_list3x.append(x3)
            coordinates_list3y.append(y3)


        return coordinates_list1x,coordinates_list1y,coordinates_list2x,coordinates_list2y,coordinates_list3x,coordinates_list3y      
    





def generate_decagon(side_length, x_center, y_center, theta, num_points):
    angles = np.linspace(0, 2 * np.pi, 10, endpoint=False) + theta
    x_vertices = x_center + side_length * np.cos(angles)
    y_vertices = y_center + side_length * np.sin(angles)
    
    x_points = np.linspace(x_vertices[-1], x_vertices[0], num_points)
    y_points = np.linspace(y_vertices[-1], y_vertices[0], num_points)
    
    x_interp = np.interp(np.linspace(0, 1, num_points), np.linspace(0, 1, 10), x_vertices)
    y_interp = np.interp(np.linspace(0, 1, num_points), np.linspace(0, 1, 10), y_vertices)
    
    return x_interp.tolist(), y_interp.tolist(), theta

def generate_triangle(side_length, x_center, y_center, theta, num_points):

    height = (np.sqrt(3) / 2) * side_length
    
    x_vertices = np.array([0, side_length / 2, -side_length / 2, 0])
    y_vertices = np.array([height / 2, -height / 2, -height / 2, height / 2])
    
    x_rot = x_vertices * np.cos(theta) - y_vertices * np.sin(theta)
    y_rot = x_vertices * np.sin(theta) + y_vertices * np.cos(theta)
    
    x = x_center + x_rot
    y = y_center + y_rot
    
    x_left = np.linspace(x[2], x[0], num_points // 3)
    y_left = np.linspace(y[2], y[0], num_points // 3)
    x_right = np.linspace(x[0], x[1], num_points // 3)
    y_right = np.linspace(y[0], y[1], num_points // 3)
    x_bottom = np.linspace(x[1], x[2], num_points // 3)
    y_bottom = np.linspace(y[1], y[2], num_points // 3)
    
    x = np.concatenate((x_left, x_right[1:], x_bottom[1:]))
    y = np.concatenate((y_left, y_right[1:], y_bottom[1:]))
    
    return x.tolist(), y.tolist(), theta

def generate_square(side_length, x_center, y_center, theta, num_points):
    half_length = side_length / 2
    
    x_vertices = np.array([-half_length, half_length, half_length, -half_length, -half_length])
    y_vertices = np.array([-half_length, -half_length, half_length, half_length, -half_length])
    
    x_rot = x_vertices * np.cos(theta) - y_vertices * np.sin(theta)
    y_rot = x_vertices * np.sin(theta) + y_vertices * np.cos(theta)
    
    x = x_center + x_rot
    y = y_center + y_rot
    
    x_left = np.linspace(x[3], x[0], num_points // 4)
    y_left = np.linspace(y[3], y[0], num_points // 4)
    x_top = np.linspace(x[0], x[1], num_points // 4)
    y_top = np.linspace(y[0], y[1], num_points // 4)
    x_right = np.linspace(x[1], x[2], num_points // 4)
    y_right = np.linspace(y[1], y[2], num_points // 4)
    x_bottom = np.linspace(x[2], x[3], num_points // 4)
    y_bottom = np.linspace(y[2], y[3], num_points // 4)
    
    x = np.concatenate((x_left, x_top[1:], x_right[1:], x_bottom[1:]))
    y = np.concatenate((y_left, y_top[1:], y_right[1:], y_bottom[1:]))
    
    return x.tolist(), y.tolist(), theta


def main(args=None):
    rclpy.init(args=args)
    service_node = ServiceNode()
    
    msg_bot_1 = Goal()
    msg_bot_2 = Goal()
    msg_bot_3 = Goal()
    
    # # #5a
    # msg_bot_1.bot_id = 1
    # msg_bot_1.x = []
    # msg_bot_1.y = []
    # for coordinate in hexagon_points:
    #    msg_bot_1.x.append(coordinate[0])
    #    msg_bot_1.y.append(coordinate[1]) 
    
    # msg_bot_1.theta = 0.0

    # msg_bot_2.bot_id = 2
    # msg_bot_2.x = []
    # msg_bot_2.y = []

    # for coordinate in rectangle_points:
    #    msg_bot_2.x.append(coordinate[0])
    #    msg_bot_2.y.append(coordinate[1]) 
    
    # msg_bot_2.theta = 0.0

    # msg_bot_3.bot_id = 3
    # msg_bot_3.x = []
    # msg_bot_3.y = []

    # for coordinate in triangle_points:
    #    msg_bot_3.x.append(coordinate[0])
    #    msg_bot_3.y.append(coordinate[1]) 

    # msg_bot_3.theta = 0.0


    ##5b

    # for coordinate in rectangle_points:
    #    msg_bot_2.x.append(coordinate[0])
    #    msg_bot_2.y.append(coordinate[1]) 
    # msg_bot_1.x,msg_bot_1.y,msg_bot_2.x,msg_bot_2.y,msg_bot_3.x,msg_bot_3.y=service_node.generate_points()
    # msg_bot_1.theta = 0.0
    # msg_bot_2.theta = 0.0
    # msg_bot_3.theta = 0.0
    # msg_bot_1.bot_id = 1
    # msg_bot_2.bot_id = 2
    # msg_bot_3.bot_id = 3
    #6
    # msg_bot_2.bot_id = 2
    # msg_bot_2.x = []
    # msg_bot_2.y = []

    image_idx=0

    while rclpy.ok():
        service_node.get_logger().info(f'countour number :{image_idx}')
        if image_idx!=len(fullimage):
            global list_update_2,pen_status_2
            if pen_status_2.data==False and list_update_2==False:
                msg_bot_2.bot_id = 2
                msg_bot_2.x = []
                msg_bot_2.y = []
                contour=fullimage[image_idx]
                prev_x=0.0
                prev_y=0.0
                for coordinate in contour:
                    distance=((coordinate[0]-prev_x)**2+(coordinate[1]-prev_y)**2)**0.5
                    if distance>spacing:
                            msg_bot_2.x.append(coordinate[0])
                            msg_bot_2.y.append(coordinate[1]) 

                            prev_x=coordinate[0]
                            prev_y=coordinate[1]
                msg_bot_2.theta = 0.0
                list_update_2=True
                image_idx+=1  
                service_node.get_logger().info(f'goal created')
            # service_node.publish_goal_2.publish(msg_bot_2)
            # service_node.get_logger().info(msg_bot_2)

            if pen_status_2.data==True and list_update_2==True:
                list_update_2=False
        if image_idx==len(fullimage):
            service_node.bot2_complete.data=True
            service_node.run_complete2.publish(service_node.bot2_complete) 
            service_node.get_logger().info(f'stup {service_node.bot2_complete}')       
        
            




        service_node.publish_goal_1.publish(msg_bot_2)    
        service_node.publish_goal_2.publish(msg_bot_2)    
        service_node.publish_goal_3.publish(msg_bot_2)    
    
        # service_node.publish_shape_1.publish(msg_shape_1)
        # service_node.publish_shape_2.publish(msg_shape_2)
        # service_node.publish_shape_3.publish(msg_shape_3)
        
        # time.sleep(1)
        rclpy.spin_once(service_node)
    rclpy.shutdown()
        
if __name__ == '__main__':
    main()

#######################################     DO NOT MODIFY THIS  FILE     ##########################################
