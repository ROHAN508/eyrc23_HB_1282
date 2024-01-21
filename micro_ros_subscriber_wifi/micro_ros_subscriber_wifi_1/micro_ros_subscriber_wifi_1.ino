#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <ESP32Servo.h>
#include <InterpolationLib.h>
//#include <Servo.h>
#include <geometry_msgs/msg/twist.h>
///

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
double rpmValues_right[19] = {-42.55,   -40.26   , -35.714, -30.76, -21.66, -13.53, -10.60, -9.81, 0  ,0,0, 10.638,13.495,16.80,25, 34.09,42.55,45.24,46.9}; //rpm
double pwmValues_right[19] = {180   ,     165  ,   150    , 135 ,  120,     105,   100,    97,   96,90, 88,  87,    80,    75,  60,  45,   30,   15,   0}; //pwm

//int constrainedRPM = constrain(abs(targetRPM), 0, 60);
//int PWMVal = Interpolation::SmoothStep(rpmValues, pwmValues, 9, constrainedRPM);

// Defining pins
#define servo1_pin  26 //right
#define servo2_pin  25  //left
#define servo3_pin  27 //rear
#define servo_pin   19  //pen
int minRPM = -57.6;      // Minimum RPM supported by the servo
int maxRPM = 57.6;       // Maximum RPM supported by the servo
int SERVO_MIN_PWM = 2500; // Minimum PWM value accepted by the servo
int SERVO_MAX_PWM = 500;// Maximum PWM value accepted by the servo

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

  
//  int constrainedRPM_right = constrain(abs(linear_x), 0, 60);


//  /int PWMVal = Interpolation::SmoothStep(rpmValues_right, pwmValues_right, 19, constrainedRPM_right);
//  /Serial.println(PWMVal);
  // Implement your control logic or kinematics here
//  inverse_kinematics(linear_x, linear_y, linear_z);
//  publish_vel(PWMVal, linear_y, linear_z);

  publish_vel(linear_x, linear_y, linear_z,angular_z);
}

int normaliseRPM(int desiredRPM) {
  int pwmValue = map(desiredRPM, minRPM, maxRPM, SERVO_MIN_PWM, SERVO_MAX_PWM);
  return pwmValue;
}

//int inverse_kinematics(double xvel, double yvel, double w){
//  // Implement your inverse kinematics here
////  w1_vel= (1/r)*(-0.33*xvel)+(0.58*yvel)+(0.0476*ang_vel);
////  w2_vel= (1/r)*(-0.33*xvel)+(-0.58*yvel)+(0.0476*ang_vel);
////  w3_vel= (1/r)*(0.66666*xvel)+(0.0476*ang_vel);
//  w1_vel = (1/r) * ( (w*d) + (-0.5*xvel) + (0.866*yvel) );
//  w2_vel = (1/r) * ( (w*d) + (-0.5*xvel) + (-0.866*yvel) );
//  w3_vel = (1/r) * ( (w*d) + (1*xvel) + (0*yvel) );
//  Serial.println(w1_vel);
//  Serial.println(w2_vel);
//  Serial.println(w3_vel);
//
//  int pwm1=normaliseRPM(w1_vel);
//  int pwm2=normaliseRPM(w2_vel);
//  int pwm3=normaliseRPM(w3_vel);
//
//  Serial.println(pwm1);
//  Serial.println(pwm2);
//  Serial.println(pwm3);
//
//  servo1.writeMicroseconds(pwm1);
//  servo2.writeMicroseconds(pwm2);
//  servo3.writeMicroseconds(pwm3);
//  
//  
//  
//  
//  return 0;  // Return value as needed
//}

void setup() {
  servo_init();
//  set_microros_wifi_transports("motorola edge 20 fusion_2495", "123456789", "192.168.173.45", 8888);
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
  delay(25);
  RCCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
  
}
