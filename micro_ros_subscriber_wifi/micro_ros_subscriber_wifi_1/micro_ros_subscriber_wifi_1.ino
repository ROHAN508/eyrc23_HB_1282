#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <ESP32Servo.h>
#include <InterpolationLib.h>
#include <geometry_msgs/msg/twist.h>


rcl_subscription_t subscriber;
geometry_msgs__msg__Twist msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

Servo servo1;
Servo servo2;
Servo servo3;
Servo micro_servo;

int targetRPM=10;


// Defining pins
#define servo1_pin  26 //right
#define servo2_pin  25  //left
#define servo3_pin  27 //rear
#define servo_pin   19  //pen

#define LED_PIN 2
double w1_vel=0;
double w2_vel=0;
double w3_vel=0;
double r=1.9;
double d=7.4;

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

void error_loop(){
  while(1){
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}
 void servo_init() {
  servo1.attach(servo1_pin);
  servo2.attach(servo2_pin);
  servo3.attach(servo3_pin);
  micro_servo.attach(servo_pin);
}

int publish_vel(int w1,int w2,int w3,int w4){
  
  servo1.write(w1);
  servo2.write(w2);
  servo3.write(w3);
  micro_servo.write(w4);

//  Serial.println(w1);
//  Serial.println(w2);
//  Serial.println(w3);
  return 0;
  
  }

void subscription_callback(const void * msgin)
{  
  const geometry_msgs__msg__Twist * msg = (const geometry_msgs__msg__Twist *)msgin;
  
  // Extract linear and angular velocities
  int linear_x = msg->linear.x;
  int linear_y = msg->linear.y;
  int linear_z = msg->linear.z;
  int angular_z= msg->angular.z;//

  

  publish_vel(linear_x, linear_y, linear_z,angular_z);
}



void setup() {
  servo_init();
//  set_microros_wifi_transports("motorola edge 20 fusion_2495", "123456789", "192.168.213.45", 8888);
  set_microros_wifi_transports("NO_INTERNET", "Qwerty@123", "192.168.0.173", 8888);
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);  
  
  delay(2000);

  allocator = rcl_get_default_allocator();

  // Create init_options
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  // Create node
  RCCHECK(rclc_node_init_default(&node, "subscriber_node_1", "", &support));

  // Create subscriber
  RCCHECK(rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist),
    "/cmd_vel/bot1"));

  // Create executor
  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
  RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &msg, &subscription_callback, ON_NEW_DATA));
}

void loop() {
  delay(50);
  RCCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
  
}
