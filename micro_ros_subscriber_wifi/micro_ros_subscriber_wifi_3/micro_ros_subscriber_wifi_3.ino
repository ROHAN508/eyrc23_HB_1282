//▪ /*
//▪ * Team Id: HB#1282
//▪ * Author List: AKSHAR DASH
//▪ * Filename: micro_ros_subscriber_wifi_3
//▪ * Theme: HologlyphBots
//▪ * Functions: publish_vel
//▪ * Global Variables: servo1_pin,servo2_pin,servo3_pin,LED_PIN
//▪ */ 
//▪ /*
//▪ * Function Name:publish_vel
//▪ * Input: wheel velocities
//▪ * Logic: gives the received pwm values to the individual servo motors
//▪ * Example Call: publish_vel(w1,w2,w3)
//▪ */ 



#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <ESP32Servo.h>
#include <InterpolationLib.h>
#include <geometry_msgs/msg/twist.h>
#include <std_msgs/msg/bool.h>  // Include the Bool message type

Servo servo1;
Servo servo2;
Servo servo3;
Servo micro_servo;

#define servo1_pin  26
#define servo2_pin  25
#define servo3_pin  27
#define servo_pin   19
#define LED_PIN     2



#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

rcl_subscription_t subscriber_cmd_vel;
rcl_subscription_t subscriber_pen_down;
geometry_msgs__msg__Twist msg_cmd_vel;
std_msgs__msg__Bool msg_pen_down;

rcl_node_t node;
rclc_support_t support;
rclc_executor_t executor;

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

int publish_vel(int w1, int w2, int w3){
  servo1.write(w1);
  servo2.write(w2);
  servo3.write(w3);
  //debug print
//  Serial.println(w1);
//  Serial.println(w2);
//  Serial.println(w3);
//  micro_servo.write(w4);
  return 0;
}

void subscription_callback_cmd_vel(const void * msgin)
{
  const geometry_msgs__msg__Twist * msg = (const geometry_msgs__msg__Twist *)msgin;
  int linear_x = msg->linear.x;
  int linear_y = msg->linear.y;
  int linear_z = msg->linear.z;
//  int angular_z = msg->angular.z;

  publish_vel(linear_x, linear_y, linear_z);
}

void subscription_callback_pen_down(const void * msgin)
{
  const std_msgs__msg__Bool * msg = (const std_msgs__msg__Bool *)msgin;
  bool pen_down = msg->data;

//  Serial.print("value:");
//  Serial.println(pen_down);

  // Do something with pen_down
  if (pen_down) {
    micro_servo.write(25);
    // Pen is down
    // Add your code here
    
  } else {
    micro_servo.write(90);
    // Pen is up
    // Add your code here
  }
}

void setup() {
  servo_init();
  set_microros_wifi_transports("motorola edge 20 fusion_2495", "123456789", "192.168.187.45", 8888);
//  set_microros_wifi_transports("NO_INTERNET", "Qwerty@123", "192.168.0.173", 8888);/
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  delay(2000);

  rcl_allocator_t allocator = rcl_get_default_allocator();

  // Create init_options
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  // Create node
  RCCHECK(rclc_node_init_default(&node, "subscriber_node_3", "", &support));

  // Create subscriber for cmd_vel topic
  RCCHECK(rclc_subscription_init_default(
    &subscriber_cmd_vel,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist),
    "/cmd_vel/bot3"));

  // Create subscriber for pen_down topic
  RCCHECK(rclc_subscription_init_default(
    &subscriber_pen_down,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),
    "/pen3_down"));

  // Create executor
  RCCHECK(rclc_executor_init(&executor, &support.context, 2, &allocator));

  // Add subscriptions to the executor
  RCCHECK(rclc_executor_add_subscription(&executor, &subscriber_cmd_vel, &msg_cmd_vel, &subscription_callback_cmd_vel, ON_NEW_DATA));
  RCCHECK(rclc_executor_add_subscription(&executor, &subscriber_pen_down, &msg_pen_down, &subscription_callback_pen_down, ON_NEW_DATA));
}

void loop() {
  RCCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
}
